# GenAI Enterprise Template

Enterprise-ready GenAI application template on AWS with RAG + Action Agents.

## What this repository includes
- AWS-native architecture for retrieval-augmented generation and tool execution
- SSO-ready identity integration and policy-driven authorization (RBAC/ABAC)
- Audit and observability standards (OpenTelemetry + Langfuse)
- Typed contracts (BAML + JSON Schema)
- CI/CD pipelines and Infrastructure as Code (Terraform)
- Helm-based Kubernetes deployments and evaluation harness

## Quick start
1. Review `docs/architecture.md` and `docs/threat-model.md`.
2. Deploy core infrastructure from `infra/terraform/envs/dev`.
3. Deploy services via `ops/helm` and configure OTEL + Langfuse.
4. Run evals in `evals/`.

## Conventions
- All placeholders are marked as `CHANGE_ME`.
- OpenAPI specs define stable service interfaces.
- All services emit OTEL traces with `traceparent` propagation.

## Security & compliance
- Authorization enforced via centralized policy service.
- Audit service records all decisions and tool executions.

## Support
Contact platform team: CHANGE_ME
