import json
import logging
import os
import uuid
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from config import get_service_name

logger = logging.getLogger("policy-service")
logging.basicConfig(level=logging.INFO, format="%(message)s")

app = FastAPI(title="Policy Service")

TOOL_ROLE_MAP = {
    "jira.create": ["admin", "user"],
    "jira.create.highrisk": ["admin"],
}


class AuthzRequest(BaseModel):
    subject: Dict[str, Any] = Field(default_factory=dict)
    resource: Optional[Dict[str, Any]] = None
    tool: Optional[Dict[str, Any]] = None
    action: str


class AuthzResponse(BaseModel):
    allow: bool
    approval_required: Optional[bool] = None
    reason: str


def setup_otel(app_ref: FastAPI) -> None:
    endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
    if not endpoint:
        return
    resource = Resource.create({"service.name": get_service_name()})
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=True))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app_ref)


@app.middleware("http")
async def add_request_context(request: Request, call_next):
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    trace_id = request.headers.get("x-trace-id")
    traceparent = request.headers.get("traceparent")
    if not trace_id:
        trace_id = traceparent or str(uuid.uuid4())
    request.state.request_id = request_id
    request.state.trace_id = trace_id

    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    response.headers["x-trace-id"] = trace_id
    return response


def get_roles_from_headers(request: Request) -> List[str]:
    roles_header = request.headers.get("x-roles", "")
    return [r.strip() for r in roles_header.split(",") if r.strip()]


def get_attributes_from_headers(request: Request) -> Dict[str, Any]:
    raw = request.headers.get("x-attributes")
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def require_context(request: Request) -> None:
    if not request.headers.get("x-tenant-id") or not request.headers.get("x-user-id"):
        raise HTTPException(status_code=400, detail="x-tenant-id and x-user-id required")


@app.post("/v1/authorize/retrieve", response_model=AuthzResponse)
async def authorize_retrieve(payload: AuthzRequest, request: Request) -> AuthzResponse:
    require_context(request)
    roles = set(get_roles_from_headers(request))
    attributes = get_attributes_from_headers(request)
    groups = set(attributes.get("groups", []))

    resource = payload.resource or {}
    acl = resource.get("acl", {})
    acl_roles = set(acl.get("roles", []))
    acl_groups = set(acl.get("groups", []))

    if roles & acl_roles or groups & acl_groups:
        return AuthzResponse(allow=True, approval_required=False, reason="allowed by acl")

    return AuthzResponse(allow=False, approval_required=False, reason="denied by acl")


@app.post("/v1/authorize/tool", response_model=AuthzResponse)
async def authorize_tool(payload: AuthzRequest, request: Request) -> AuthzResponse:
    require_context(request)
    roles = set(get_roles_from_headers(request))

    tool = payload.tool or {}
    tool_name = tool.get("name") or tool.get("operation") or "unknown"
    allowed_roles = set(TOOL_ROLE_MAP.get(tool_name, []))

    if not allowed_roles:
        return AuthzResponse(allow=False, approval_required=False, reason="unknown tool")

    if not roles & allowed_roles:
        return AuthzResponse(allow=False, approval_required=False, reason="role not allowed")

    approval_required = False
    if tool.get("risk_level") == "high" and "admin" not in roles:
        approval_required = True

    return AuthzResponse(
        allow=True,
        approval_required=approval_required,
        reason="approved" if not approval_required else "approval required",
    )


setup_otel(app)
