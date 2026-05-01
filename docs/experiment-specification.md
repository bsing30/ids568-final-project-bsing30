# Offline A/B experiment spec

## Guess I'm testing
Variant B tweaks retrieval + prompting for the classifier. Hypothesis: it bumps SLA-resolution-ish success vs A by ≥3 pts without dragging latency past the guardrails baked into monitoring configs.

## What I cared about counting
Primary: SLA-resolution proxy (Bernoulli per interaction).

Sides: simulated latency pulls, escalation flag, coarse groundedness heuristic from audit passes.

Rough business read: happier first-pass routing + fewer escalations.

## Assignment / randomization
Hash session IDs mod 2 for 50/50 so retries stick to same arm unless you purposely rotate sessions.

## How big / how long
Used baseline p≈0.62, wanna catch ~3 pts MDE at α=.05 power ~0.8 → ballpark ~4k samples each side (formula's in code). Assuming ~600 real sessions/day, you're looking ~2-ish weeks—not holy writ if traffic differs.

## Stats plan (keep it sane)
Primary diff: pooled two-proportion z + Wald CI printed in simulator.

Extras: Welch t-test on latency distributions; escalate/groundedness treated sanity-check tier because multiplicity gets messy fast.

Decision story: nail primary hypothesis first (reject if CI straddles 0 awkwardly).

Then stare at latency + escalation—don't ship B just because auxiliary tests fluke unless you honestly pre-committed to them being gates.

Bonferroni exists if graders care; realistically I prioritized the SLA metric unless we formalized secondaries upfront.
