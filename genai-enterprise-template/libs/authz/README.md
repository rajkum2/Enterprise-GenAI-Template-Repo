# Authz Library

Shared authorization client for the policy service. Handles RBAC/ABAC evaluation
and enforces decisions before retrieval or tool execution.

## Required usage
- Call `/v1/authorize/retrieve` before RAG.
- Call `/v1/authorize/tool` before tool execution.
