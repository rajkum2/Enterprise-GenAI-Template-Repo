import hashlib
import json
import logging
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import psycopg
from psycopg.types.json import Jsonb
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from config import get_service_name

logger = logging.getLogger("audit-service")
logging.basicConfig(level=logging.INFO, format="%(message)s")

app = FastAPI(title="Audit Service")

REDACT_KEYS = {"authorization", "token", "prompt"}


class AuditEvent(BaseModel):
    event_type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    tenant_id: Optional[str] = None


class AuditEventsRequest(BaseModel):
    events: List[AuditEvent]


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


def hash_value(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def redact_payload(value: Any) -> Any:
    if isinstance(value, dict):
        redacted = {}
        for key, val in value.items():
            if key.lower() in REDACT_KEYS:
                redacted[key] = {"hash": hash_value(val)}
            else:
                redacted[key] = redact_payload(val)
        return redacted
    if isinstance(value, list):
        return [redact_payload(item) for item in value]
    return value


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


def require_tenant(request: Request) -> str:
    tenant_id = request.headers.get("x-tenant-id")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="x-tenant-id required")
    return tenant_id


@app.post("/v1/audit/events")
async def ingest_events(payload: AuditEventsRequest, request: Request) -> Dict[str, str]:
    tenant_id = require_tenant(request)
    if request.headers.get("x-request-id") and len(payload.events) != 1:
        raise HTTPException(status_code=400, detail="x-request-id supports single event")

    event = payload.events[0]
    if event.tenant_id and event.tenant_id != tenant_id:
        raise HTTPException(status_code=400, detail="tenant_id mismatch")

    event_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    cleaned_payload = redact_payload(event.payload)
    audit_payload = {
        "tenant_id": tenant_id,
        "event_type": event.event_type,
        "payload": cleaned_payload,
    }

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise HTTPException(status_code=500, detail="DATABASE_URL required")

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO audit_events (id, tenant_id, event_type, payload) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                (event_id, tenant_id, event.event_type, Jsonb(cleaned_payload)),
            )
        conn.commit()

    audit_path = os.environ.get("AUDIT_LOCAL_PATH", "./data/audit")
    os.makedirs(audit_path, exist_ok=True)
    date_str = datetime.utcnow().strftime("%Y%m%d")
    file_path = os.path.join(audit_path, f"audit-{date_str}.jsonl")
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps({"id": event_id, **audit_payload}) + "\n")

    return {"event_id": event_id}


setup_otel(app)
