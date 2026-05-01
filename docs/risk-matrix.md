# Risk Matrix

| Risk | Likelihood (1-5) | Severity (1-5) | Score | Mitigation Plan |
|---|---:|---:|---:|---|
| Prompt injection via retrieved text | 3 | 5 | 15 | Source allowlist, retrieval sanitizer, response policy checks |
| Drift-driven performance regression | 4 | 4 | 16 | PSI alerts, automatic retraining gate, canary rollout |
| PII leakage in logs | 2 | 5 | 10 | Regex/entity redaction, encrypted storage, short retention |
| Bias against minority language style | 3 | 4 | 12 | Fairness slices, targeted data augmentation, HITL escalation |
| Auditability gaps in release process | 2 | 4 | 8 | Mandatory approvals, immutable audit trail, quarterly control review |
