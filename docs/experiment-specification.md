# Experiment Specification

## Hypothesis
Variant B (prompt+retrieval tuning) improves SLA-resolution rate compared to baseline Variant A by at least 3 percentage points without increasing latency beyond guardrail limits.

## Success Metrics
- **Primary:** SLA-resolution rate (binary success metric).
- **Secondary / guardrail:** median latency on the inference path (continuous), groundedness-proxy pass rate from spot audits (binary), escalation rate triggered by unresolved intent (binary).
- **Business KPI:** percent of tickets auto-routed correctly on first pass (maps to SLA-resolution uplift + escalation reduction).

## Randomization Method
User sessions are randomly assigned using deterministic hashing of session ID modulo 2, resulting in a 50/50 split and preventing assignment drift across retries.

## Sample Size and Duration
Assumptions: baseline success=0.62, MDE=0.03, alpha=0.05, power=0.8, Bernoulli std ~0.48. Required per-variant sample size is approximately 4,019 observations. With expected 600 sessions/day, total duration is about 14 days.

## Statistical Plan
### Primary KPI (Bernoulli)
- Explicit two-proportion z-test for `p_B - p_A` on SLA-resolution outcomes.
- 95% Wald confidence interval for the difference in proportions.

### Guardrail metrics (continuous + secondary Bernoulli)
- Latency: Welch two-sample t-test on simulated per-request latency samples (secondary operational signal).
- Escalation + groundedness proxy: treated as exploratory unless pre-registered because multiple comparisons inflate false-positive risk.

### Multiple hypothesis control (primary vs guardrail metrics)
- **Primary hypothesis is tested once** at alpha `0.05`: approve Variant B on SLA uplift if `p_primary < 0.05` and the CI excludes 0 favoring B.
- **Guardrails are evaluated hierarchically:**
  - If primary passes, Variant B **must still** satisfy non-inferiority on latency (mean latency not worse than A by > 50ms surrogate) **and**
  - must not regress escalation rate materially (difference must favor B unless explained by taxonomy changes).
- If multiple secondary metrics were treated as simultaneous gates, a Bonferroni correction (`alpha_adjusted = 0.05 / m`) tightens thresholds; here we prioritize the primary SLA metric and interpret secondaries cautiously unless explicitly pre-committed.
