# Ingestion Service

## Responsibilities
- Ingest documents from sources and index into OpenSearch.
- Provide index status for operations.

## Required environment variables
- `OTEL_EXPORTER_OTLP_ENDPOINT`
- `OTEL_SERVICE_NAME=ingestion-service`
- `OPENSEARCH_ENDPOINT`
- `S3_BUCKET`
