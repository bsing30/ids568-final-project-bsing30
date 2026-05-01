# Governance Review

## NIST AI RMF framing (informative)
For organization, this writeup groups controls under the familiar NIST AI RMF functions (Govern / Map / Measure / Manage). It is **not** a formal compliance attestation.
- **Govern:** release gates, approvals, and escalation path (CTO memo + `logs/audit-trail.jsonl`)
- **Map:** retrieval + classifier boundary and workflow automation risks (`docs/system-boundary-diagram.png`)
- **Measure:** monitoring and drift signals referenced in `dashboards/` plus `docs/drift-diagnostic-report.md`
- **Manage:** canary/rollback posture, retrieval hygiene, and fairness slice practices listed in registers/matrices

The README and artifact paths above are the concrete records of what would be audited in practice.

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
