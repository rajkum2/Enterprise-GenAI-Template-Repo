# Incident Response Runbook

## Scope
This runbook covers detection, containment, remediation, and post-incident review.

## Steps
1. Triage incident severity and notify on-call (CHANGE_ME).
2. Contain: disable offending integrations and revoke tokens.
3. Mitigate: apply hotfix or rollback via helm release.
4. Audit: verify access logs and generate event report.
5. Post-incident: conduct RCA within 72 hours.
