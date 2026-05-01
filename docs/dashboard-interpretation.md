# Dashboard interpretation (simulated metrics)

Ran fake traffic locally to paint the charts—same idea you'd use hooked to a real service.

## What I see
Throughput hovers roughly 18–24 RPS. Median-ish latency landed under ~120 ms during the synth run—not amazing, but fine for internal routing if your SLA backs that up.

Errors floated ~2.5–4% unless I spammed bursts; drift creeps upward as I shift simulated phrasing/category mix later in the run.

## What I'd worry about in prod
Heavy tails before the average moves (cache misses, sluggish deps upstream).

Malformed payloads clustered with anomalies—might be schema drift or bots.

Drift creeping up silently before accuracy tanks.

## Alerts I'd wire (same vibes as Grafana JSON + rules YAML)
Warn if rolling error clears ~5% for ~10 min.

Ping hard if synthetic P95 path crosses ~300 ms for ~5 min (match what we drew on Grafana).

Kick a drift drill if engineered drift gauge sits > ~0.25 for a handful of buckets.

Treat input anomalies > ~8% over 15 min as “data pipes broken,” not model-only.

## Why Prometheus/Grafana OSS here
They're free, Prometheus understands histogram buckets for latency tails, Grafana is quick to slap panels on. Gauges/errors/drift/anomalies line up how I'd actually ops this.

## Supporting files (where the configs lived)
See `dashboards/prometheus.yml`, `dashboards/grafana-dashboard.json`, `dashboards/prometheus-rules.yml`.

