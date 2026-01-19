# Threat Model

## Key threats and mitigations

### Prompt injection
- Use system prompts that are non-overridable and place tool usage behind policy checks.
- Strip or quarantine untrusted context from retrieval results.

### Data exfiltration
- Enforce strict allow-lists for tool execution and retrieval scopes.
- Apply output filtering and logging redaction for sensitive data.

### Unauthorized retrieval/tool execution
- Centralized `policy-service` performs RBAC/ABAC checks.
- Orchestrator requires explicit approval via `/v1/tasks/{id}/approve`.

### Logging redaction
- OTEL processor `redact` removes PII/PHI before export.
- Audit logs store hashed identifiers where possible.

### Idempotency and replay
- Use idempotency keys on tool execution and ingestion endpoints.
- Validate nonce/time-bound tokens for approvals.

### Supply chain controls
- Container signing and SBOM checks in CI/CD.
- Terraform module pinning and dependency lockfiles.
