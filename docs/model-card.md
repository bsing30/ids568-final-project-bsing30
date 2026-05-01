# Model card — support intent classifier (v1.3)

Think of this as “what it is” + “what it’s bad at” for a classifier that guesses ticket intent before routing.

## What it is
- Smaller transformer-style classifier plus retrieval/context (conceptually—this repo is wired for instrumentation + demos, not a full trainer).
- Served from a Python API; batch cap 16 was the assumption when I wrote sizing notes.
- v1.3 is what the A/B sim compares against baseline.

## Numbers I lean on offline
Held-out validation (time split): accuracy ~0.89, macro F1 ~0.86 — good enough that I’d bother monitoring drift.

**A/B simulation** (`python src/ab_test/simulation.py`, ~4019 requests/side):  
Variant B beat A on SLA-resolution-ish proxy (~65.5% vs ~61.6%) with z-test output in the terminal. Secondary stuff from the same run: fewer escalations, slightly better “would this pass audit” heuristic, latency mean somewhat lower (~195 ms vs ~223 ms simulated). Grain of salt: simulator is biased on purpose.

**Latency:** targeting P95 under 300 ms in prod (see Grafana/Prometheus thresholds in `dashboards/`).

## Training data
Synthetic/de-ID mix; intents = billing / technical / account / escalation. Split by calendar week so I don’t leak future weeks into validation. Didn’t keep raw PII in artifacts.

## Where it screws up
- Weird product names, slang, other languages → more errors.

- Routing taxonomy jumps (new ticket types) confuse it.

- One-liner ambiguous tickets flip labels.

- If retrieval KB is stale or junk sneaks into the corpus, retrieval makes misroutes worse, not better.

## Ethical-ish stuff worth saying
Minority phrasing buckets can lose out if counts are uneven. Wrong intent = annoyed customers waiting on support.

## Intended use vs not
**In scope:** first-pass routing for internal support tooling, with escalation when confidence is junk or queues look weird.

**Out of scope:** legal decisions, HR, healthcare triage, “fully automated” replies to users with no oversight.
