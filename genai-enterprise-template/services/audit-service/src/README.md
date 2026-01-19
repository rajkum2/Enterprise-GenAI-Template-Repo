# Audit Service

## Responsibilities
- Ingest audit events from all services.
- Persist immutable audit logs for compliance.

## Required environment variables
- `OTEL_EXPORTER_OTLP_ENDPOINT`
- `OTEL_SERVICE_NAME=audit-service`
- `AUDIT_STORE_DSN`

## Local run

Endpoint:
- `POST /v1/audit/events`

Required headers:
- `x-tenant-id`
- Optional: `x-request-id`, `traceparent` or `x-trace-id`

Environment variables:
- `DATABASE_URL`
- `OTEL_EXPORTER_OTLP_ENDPOINT`
- `OTEL_SERVICE_NAME=audit-service`
- `AUDIT_LOCAL_PATH` (default: `./data/audit`)

Run:
- `uvicorn main:app --host 0.0.0.0 --port 8080`
