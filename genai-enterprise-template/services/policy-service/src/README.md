# Policy Service

## Responsibilities
- Evaluate RBAC/ABAC policies for retrieval and tool execution.
- Provide centralized authorization decisions.

## Required environment variables
- `OTEL_EXPORTER_OTLP_ENDPOINT`
- `OTEL_SERVICE_NAME=policy-service`
- `AURORA_DSN`

## Local run

Endpoints:
- `POST /v1/authorize/retrieve`
- `POST /v1/authorize/tool`

Required headers:
- `x-tenant-id`, `x-user-id`
- Optional: `x-roles`, `x-attributes`, `traceparent` or `x-trace-id`

Environment variables:
- `OTEL_EXPORTER_OTLP_ENDPOINT`
- `OTEL_SERVICE_NAME=policy-service`

Run:
- `uvicorn main:app --host 0.0.0.0 --port 8080`
