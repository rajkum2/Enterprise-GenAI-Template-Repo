# Orchestrator Service

## Responsibilities
- Handle `/v1/chat` and task management endpoints.
- Coordinate policy checks, retrieval, LLM calls, and tool execution.
- Emit audit events for all decisions and tool usage.

## Required environment variables
- `OTEL_EXPORTER_OTLP_ENDPOINT`
- `OTEL_SERVICE_NAME=orchestrator-service`
- `POLICY_SERVICE_URL`
- `RAG_RETRIEVAL_URL`
- `LLM_GATEWAY_URL`
- `AUDIT_SERVICE_URL`
