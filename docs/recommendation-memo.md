# Recommendation memo (A/B simulation)

## Call
I'd roll out **variant B**, but capped at ~25% of traffic until the next checkpoint.

## Why
Simulation run from `simulation.py` shows B beating A on the main SLA-ish success metric (z-test clears the usual 0.05 bar; CI favors B). The side metrics also look sane: escalations drop a bit, the cheap groundedness heuristic improves, simulated latency dips. Not proof of magic—just consistent with “prompt + retrieval tweak helped routing.”

## Before opening the floodgates
- Keep the hard rollback if errors stay above ~5% or P95 slips past ~300 ms.
- If escalation or groundedness flips sideways in prod, freeze the rollout and figure out whether it's data vs model before going past the canary.
- Log outcomes another week-ish so weekday vs weekend doesn't fool you.

- Keep a small A holdout after launch—you want something to sanity compare against.

