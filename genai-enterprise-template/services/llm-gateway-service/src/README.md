# LLM Gateway Service

## Responsibilities
- Centralize LLM provider access and model routing.
- Apply safety checks and redaction policies.
- Emit metrics and trace spans for model calls.

## Required environment variables
- `OTEL_EXPORTER_OTLP_ENDPOINT`
- `OTEL_SERVICE_NAME=llm-gateway-service`
- `MODEL_PROVIDER=CHANGE_ME`
- `MODEL_API_KEY=CHANGE_ME`
