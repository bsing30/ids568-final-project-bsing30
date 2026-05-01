# Governance review (support routing stack)

Borrowing NIST AI RMF wording only as section labels—not claiming we passed audits.

Govern / approvals / escalation → CTO memo + JSONL audit trail snippets.

Mapping risks / architecture → classifier + retrieval diagram PNG.

Measure → Grafana/Prometheus JSON + drift report.

Manage → rollout/cleanup habits described in matrices + CTO memo bullets.


## Data Security
- Inference logs are redacted for direct identifiers before storage.
- Access to model artifacts and logs is role-based and audited.
- Retention defaults to 30 days for operational telemetry.

## Retrieval Risks
- Exposure risk if stale or untrusted retrieval documents are indexed.
- Contamination risk from incorrectly labeled support macros.
- Stale-knowledge risk when product policy pages are not refreshed.
Mitigations include source allowlists, freshness checks, and index version pinning.

## Hallucination Risk Points
- Ambiguous ticket language can produce overconfident but incorrect intent labels.
- Low-context prompts increase the chance of unsupported rationale text.
Mitigation: confidence thresholding and human fallback for uncertain predictions.

## Tool-Misuse Pathways
- Incorrect route-to-system calls may trigger wrong workflow automations.
- Bulk retry loops can amplify failures under upstream degradation.
Mitigation: policy engine checks and rate-limited tool execution.

## Compliance Concerns
- Potential PII handling violations in free-text support requests.
- Need for explainable routing rationale for audit response.
Mitigation: PII filtering, structured decision trace, periodic compliance review.
