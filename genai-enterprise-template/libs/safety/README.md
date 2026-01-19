# Safety Library

Contains guardrails for prompt injection detection, output filtering, and
redaction policies. Used by the LLM gateway and orchestrator.

## Required usage
- Run safety checks before model invocation.
- Redact sensitive data before logging or audit export.
