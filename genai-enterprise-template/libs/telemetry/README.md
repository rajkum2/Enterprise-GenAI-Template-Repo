# Telemetry Library

Provides shared OpenTelemetry helpers, propagation configuration, and trace context
utilities for all services. Services must configure OTEL exporters and use the
same `traceparent` propagation headers.

## Required usage
- Set `OTEL_EXPORTER_OTLP_ENDPOINT`.
- Set `OTEL_SERVICE_NAME` to the service identifier.
- Use W3C trace context propagation.
