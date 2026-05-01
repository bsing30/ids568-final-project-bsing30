# Experiment specification (offline sim)

Plain-language version of what the assignment asks for: hypothesis, metrics, randomization, sample size, and how I’ll read the statistics.

## Hypothesis
Variant B (retrieval + prompt tuning) bumps the SLA-resolution proxy vs variant A by at least ~3 percentage points, without violating the latency/error guardrails you’d watch on Grafana.

## Success metrics (match the rubric list)
Primary: SLA-resolution proxy (Bernoulli; “did this route resolve inside our SLA-ish window”).  
Secondary / guardrails: simulated latency draws, escalation flag (“had to escalate / hand off”), cheap groundedness pass rate from mocked audits.

Business KPI (same spirit as the checklist): happier first-shot routing plus fewer escalations—mirrors SLA + escalation pair above.

## Randomization method
Session IDs hash mod two → deterministic 50/50 split so repeat requests land in the same arm unless you regenerate sessions intentionally.

## Required sample size and duration (power sketch)
Assume baseline success ≈0.62, MDE ≈0.03, α=0.05, power ≈0.8, pooled Bernoulli SD ≈0.48 → ~4k sessions per variant (same math surfaced in `src/ab_test/simulation.py`). Ballpark timeline if you honestly see ~600 sessions/day ≈two weeks—adjust if throughput differs.

## Statistical evaluation
Primary KPI: pooled two-sample proportion z-test with Wald CI printed by the simulator.  
Latency: Welch t-test on sampled latencies because it isn’t Bernoulli.  
Escalation + groundedness: sanity-check guardrails since testing everything at α=.05 invites false positives—I lead with the SLA primary, glance at latency/escalations second, Bonferroni-style correction only if multiple metrics were contractual gates upfront.
