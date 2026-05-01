# Model Card: Support Intent Classifier (v1.3)

## Model Details
- **Model type:** Distilled transformer classifier with retrieval-augmented context features.
- **Serving mode:** Python API with batch size up to 16 requests.
- **Version:** v1.3 (candidate release evaluated in A/B test).

## Performance
- Validation accuracy (holdout temporal split): 0.89
- Macro F1 (intent labels): 0.86
- **Primary rollout KPI proxy (offline A/B simulation, `n≈4019` per variant, seed-stable):**
  - Variant A SLA-resolution rate: ~0.6156
  - Variant B SLA-resolution rate: ~0.6551
  - Statistically significant uplift on primary intent-routing SLA proxy (explicit two-proportion z-test reported by `python src/ab_test/simulation.py`)
- **Operational guardrail metrics from the same simulation run:**
  - Escalation rate: A ~11.84% vs B ~8.86% (fewer unresolved/misclassified paths)
  - Groundedness proxy (human audit passes): A ~76.86% vs B ~81.46%
  - Mean inference latency surrogate: A ~223.5 ms vs B ~195.1 ms (**non-inferior / improved** versus A under the surrogate generator)
- P95 latency SLO guardrail remains **< 300 ms** for production rollout (validated by monitoring dashboards and histogram buckets)

## Training Data
- Synthetic + de-identified support-ticket corpus (intent labels: billing, technical, account, escalation).
- Temporal split by week to reduce leakage.
- No direct PII retained in training artifacts.

## Limitations and Failure Modes
- Degrades with unseen product names or multilingual slang.
- Sensitive to abrupt taxonomy changes in downstream routing categories.
- Higher uncertainty on short/ambiguous inputs.
- Retrieval-dependent misroutes increase when KB sections are stale, incorrectly labeled macros leak into retrieval, or new products lack indexed documentation.

## Ethical Risks and Considerations
- Class imbalance can under-route minority issue categories.
- Misclassification may delay user support resolution.
- Potential fairness concerns across language styles.

## Intended Use
Automated first-pass intent routing for customer support operations, with human escalation for low-confidence outputs.

## Out-of-Scope Use
Not approved for legal decision-making, hiring, healthcare triage, or fully autonomous user-facing responses.
