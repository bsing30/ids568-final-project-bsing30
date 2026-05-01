# IDS568 — Module 8 final project

Support ticket **intent routing** toy system (**synthetic / demo traffic only**). Grafana + Prometheus scrape configs, drift scripts + plots, offline A/B sim, model card + governance memos.

## What's in each folder
- `src/monitoring/`: Prometheus metrics helpers + fake traffic generator
- `src/ab_test/`: A/B experiment simulation and statistical analysis
- `src/drift/`: data integrity checks and drift detection analysis
- `dashboards/`: Prometheus and dashboard configuration assets
- `docs/`: writeups per assignment parts (C1–C5)
- `logs/`: structured audit trail
- `visualizations/`: generated charts and dashboard/drift evidence

## Setup
1. Create environment:
   - `python -m venv .venv && source .venv/bin/activate`
2. Install dependencies:
   - `pip install -r requirements.txt`

## Reproduction
1. **Component 1 (Monitoring)**
   - `python src/monitoring/instrumentation.py`
   - Optional local `/metrics` server (recommended for Grafana/Prometheus scraping demo):
     - `METRICS_SERVE_PORT=8002 python src/monitoring/metrics_exporter.py` (runs until stopped)
     - `METRICS_SERVE_PORT=8002 python src/monitoring/simulate_traffic.py`
   - Prometheus alert rules (optional): `dashboards/prometheus-rules.yml`
2. **Component 2 (A/B Test)**
   - `python src/ab_test/simulation.py`
3. **Component 4 (Drift Detection)**
   - `python src/drift/drift_detection.py`
4. Open generated figures in `visualizations/` and read linked docs in `docs/`.

## Component Links
- C1: `src/monitoring/`, `dashboards/`, `docs/dashboard-interpretation.md`, `visualizations/dashboard-screenshot.png`
- C2: `src/ab_test/simulation.py`, `docs/experiment-specification.md`, `docs/recommendation-memo.md`
- C3: `docs/model-card.md`, `docs/risk-register.md`, `docs/lineage-diagram.png`, `logs/audit-trail.jsonl`
- C4: `src/drift/drift_detection.py`, `visualizations/drift_over_time.png`, `docs/drift-diagnostic-report.md`
- C5: `docs/governance-review.md`, `docs/risk-matrix.md`, `docs/system-boundary-diagram.png`, `docs/cto-memo.md`

## Lessons learned (short)
Metrics don't help if alerts don't map to anyone's job (“now what?”). Drift graphs are the same—they're only actionable if ops knows when to freeze or queue a retrain. Governance pages should match what's actually enforced at release—not a stack of screenshots nobody reads.
