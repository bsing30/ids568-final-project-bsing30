# Recommendation Memo

## Decision
**Ship Variant B to staged rollout (25% traffic) with guardrails enabled.**

## Rationale
The simulation shows a statistically significant improvement on the **primary SLA-resolution rate** (two-proportion z-test, `p < 0.05`, CI fully above 0 favoring B), with supporting improvements on guardrail metrics (lower escalation, higher groundedness proxy, lower mean latency). This pattern is consistent with the intended effect of prompt+retrieval tuning for the support-intent classifier.

## Conditions
- Keep canary rollback trigger if error rate exceeds 5% or P95 latency exceeds 300 ms.
- Treat secondary metrics as **guardrails**: if escalation or groundedness unexpectedly diverge under live traffic, pause rollout and root-cause before expanding beyond the canary.
- Continue experiment logging for one additional week to verify stability across day-of-week traffic patterns.
- Maintain holdout cohort for post-launch comparison.
