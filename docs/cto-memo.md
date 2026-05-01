# Short memo for CTO — support intent routing

## TL;DR
Fine to ship incremental traffic if drift + alerting stay boring. Retrieval junk and slow regression when traffic mix changes worry me more than raw accuracy numbers from a leaderboard.

## What I'd actually fund next
1. **Drift playbook:** PSI over ~0.2 for a few rolling windows ⇒ someone opens a ticket, runs the drift script, decides retrain vs data fix—not “wait until users complain.”
2. **Canary discipline:** automate rollback hooks off error band + latency (same thresholds we sketched on the dashboard memo).
3. **KB/source hygiene:** who owns doc freshness when products ship weekly? Retrieval without owners rots fast.
4. **Quarter-ish governance touchpoint:** quick fairness slice review isn’t flashy but keeps you honest.

Green light for phased rollout on B assuming there’s a real owner for paging through alerts—you don’t learn anything from Grafana if nobody reacts.

## When humans jump in

**Tier 1 — auto:** Confidence ok, gauges normal. Let tooling route tickets.

**Tier 2 — review queue:** Weird confidence OR drift creeping OR burst of malformed payloads → human eyeballs it; attach whatever trace you logged.

**Tier 3 — pager:** Probable abusive prompt/tool path, nasty policy category, latency/error SLA blown → halt automation until eng + whoever owns governance signs off.

**Timing:** Aim for Tier-2 turnaround ~1 hr business hours (we said ~4 hr nights/weekends as placeholder). Tier-3 = page instantly if it’s sticking per `prometheus-rules.yml` / dashboard triggers.

