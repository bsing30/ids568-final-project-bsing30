# Drift diagnostic writeup

Toy setup: twelve rolling windows comparing “reference-ish” embeddings vs creeping production-ish draws, plus categorical intent percentages shifting over time (`billing`, `technical`, `account`, `escalation`). Script emits `psi_primary`, `psi_secondary`, canned label PSI, mashed into `psi_aggregate` so one line can mimic what you'd plot on infra dashboards.

Late windows PSI clears ~0.2 (my “squint harder” cutoff) while KS reads basically “yeah these aren't the same distro anymore.”

## What moved most
Primary synthetic feature steadily walks upward each window—cheap stand-in for phrasing centroid drift.

Secondary feature drifts with it because correlation noise ramps (think logging quirks).

Label mix slips: escalation share grows at the expense of technical-ish intents (launch noise vs outage chatter story).

Label mix caveat: categories can drift before embeddings scream if ticket taxonomy owners churn faster than the vector corpus updates.

## If this were production, what's the sting?
Heavy escalation traffic usually means nastier prompts + longer human loops, so autopilot suffers first.

Finger-in-the-air once aggregate PSI hugs ~0.28–0.37:

macro-F1 might shed ~4–8 pts versus quiet weeks,

SLA-style success might slip ~2–5 pts mainly because reviewers bounce tickets,

Queues stretch when escalations hog agents,

Small routing slices (billing vs technical) silently rot if imbalance worsens—worth slicing dashboards, not trusting global aggregates.

Plots + CSV proofs: `visualizations/drift_over_time.png`, `visualizations/drift_summary.csv`.

## What I'd do ops-wise
Freeze promotion + open retrain/data ticket once PSI rides > 0.2 three windows straight.

Normalize weird vocabulary bursts if product marketing drops new SKUs weekly.

Actually monitor per-intent metrics—not just PSI soup.

Abort rollouts when drift ramps while A/B guardrails flip red simultaneously.

## Link to monitoring chatter
Higher drift PSI should flirt with Prometheus drift gauge + anomaly counter before error rate screams—alerts templated loosely in `dashboards/prometheus-rules.yml`.
