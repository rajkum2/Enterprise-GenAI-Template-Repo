# Disaster Recovery Plan

## Recovery objectives
- RTO: 4 hours
- RPO: 15 minutes

## Strategy
- Multi-AZ Aurora, OpenSearch snapshots, and S3 versioning.
- EKS cluster redeploy using Terraform + Helm.

## Steps
1. Restore data stores from snapshots.
2. Recreate infra and redeploy services.
3. Validate critical endpoints and run smoke tests.
