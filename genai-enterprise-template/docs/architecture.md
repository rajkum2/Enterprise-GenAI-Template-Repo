# Architecture

## Service roles
- `orchestrator-service`: entrypoint for chat and task execution, coordinates RAG + tools.
- `llm-gateway-service`: central LLM invocation layer with provider routing and safety gates.
- `rag-retrieval-service`: retrieval service for vector + keyword search and reranking.
- `ingestion-service`: offline ingestion and indexing of documents into OpenSearch.
- `policy-service`: RBAC/ABAC authorization and policy decisions for retrieval/tools.
- `connector-jira-service`: action agent integration for Jira ticket creation.
- `audit-service`: audit event intake for decisions, access, and tool execution.

## Online flow (chat + actions)
1. Client calls `orchestrator-service` `/v1/chat`.
2. Orchestrator calls `policy-service` for retrieval and tool authorization.
3. Orchestrator calls `rag-retrieval-service` for contextual grounding.
4. Orchestrator calls `llm-gateway-service` for model generation.
5. If tool execution is approved, orchestrator calls `connector-jira-service`.
6. All actions emit audit events to `audit-service`.

## Offline flow (ingestion)
1. `ingestion-service` ingests documents from S3 or sources.
2. `ingestion-service` writes embeddings + metadata into OpenSearch.
3. Audit events are emitted for ingestion and indexing changes.

## Data plane
- Storage: S3 (documents), OpenSearch (vectors + metadata), Aurora (policy data), Redis (caching).
- Compute: EKS for services and workers.
- Networking: VPC with private subnets; IRSA for pod IAM roles.
- Observability: OTEL collector -> AWS X-Ray + CloudWatch (EMF) + Langfuse.

## SLO targets
- Chat availability: 99.9% monthly.
- Chat p95 latency: < 4s (excluding tool execution).
- Retrieval p95 latency: < 400ms.
- Authorization p95 latency: < 100ms.
- Audit ingestion success: 99.99% of events.

## Environment strategy
- `dev`: sandbox with relaxed quotas and synthetic data.
- `stage`: production-like environment for load and security testing.
- `prod`: locked down, audited, least-privilege policies.
- All environments use identical helm charts with env-specific values.
