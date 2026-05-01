# IDS568 — Module 8 final project (monitoring & governance)

## Overview
This repo is the Module 8 capstone for a synthetic **customer-support intent routing** system. It covers monitoring, an offline A/B simulation, drift checks, model documentation, and a system-level risk review.

## Project Structure
- `src/monitoring/`: API metrics instrumentation and synthetic traffic generator
- `src/ab_test/`: A/B experiment simulation and statistical analysis
- `src/drift/`: data integrity checks and drift detection analysis
- `dashboards/`: Prometheus and dashboard configuration assets
- `docs/`: all written deliverables for Components 1-5
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

## Lessons Learned
- Operational metrics must map to intervention playbooks, not just dashboards.
- Drift signals are only useful when connected to business impact and retraining triggers.
- Governance artifacts are strongest when tied directly to monitored behavior and release gates.
- A/B testing rigor (power, effect size, confidence intervals) prevents premature rollouts.
