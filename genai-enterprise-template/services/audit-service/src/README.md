# Audit Service

## Responsibilities
- Ingest audit events from all services.
- Persist immutable audit logs for compliance.

## Required environment variables
- `OTEL_EXPORTER_OTLP_ENDPOINT`
- `OTEL_SERVICE_NAME=audit-service`
- `AUDIT_STORE_DSN`
