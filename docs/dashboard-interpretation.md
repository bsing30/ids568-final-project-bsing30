# Dashboard Interpretation

## System Health Findings
The simulated production dashboard shows stable request volume (roughly 18-24 RPS) and median latency under 120 ms, which is acceptable for an internal support-routing workflow. Error rate is mostly between 2.5% and 4.0%, with occasional spikes around traffic bursts.

## Bottlenecks and Risks
- **Latency tail risk:** P95 latency rises when synthetic traffic ramps and cache hit behavior degrades.
- **Error concentration:** Error spikes align with high anomaly windows, suggesting malformed payload handling is a reliability bottleneck.
- **Data quality degradation:** Drift score trends upward over time, indicating distribution shift in user phrasing and ticket category frequency.

## Alert Triggers for Production
- Trigger warning when `prediction_error_rate > 0.05` for 10 minutes.
- Trigger critical alert when P95 latency > 300 ms for 5 minutes.
- Trigger drift investigation when `feature_drift_score > 0.25` sustained for 3 windows.
- Trigger data-quality incident when input anomaly rate > 8% over rolling 15-minute window.

## Design Justification
Prometheus + Grafana was selected for OSS compatibility, low setup overhead, and strong support for histogram-based latency tracking. The selected metrics map to operational outcomes: latency and throughput for user experience, error/integrity for reliability, and drift for forward-looking model health.

## Supporting files
- `dashboards/prometheus.yml` — Prometheus scrape config (`/metrics`; default target `localhost:8002` when using the local exporter in the README)
- `dashboards/grafana-dashboard.json` — Grafana dashboard export (P95 latency panels with a 300 ms reference line; stat panels for quick checks)
- `dashboards/prometheus-rules.yml` — example alert rules (Prometheus must be configured separately to load/evaluate rule files)
