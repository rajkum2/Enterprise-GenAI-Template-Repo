# ADR 0001: AWS + EKS + OpenSearch

## Status
Accepted

## Context
We require a production-grade GenAI platform with strong security and observability.

## Decision
Adopt AWS EKS for compute, OpenSearch for retrieval, and central policy/audit services.

## Consequences
- Consistent deployment via Helm and Terraform.
- Single-vendor operational model with managed services.
