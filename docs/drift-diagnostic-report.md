# Drift Diagnostic Report

## Summary
Drift analysis across 12 windows combines **numerical embedding aggregates** (`psi_primary`, `psi_secondary`) with a **label-mix PSI** from categorical intents (`billing`, `technical`, `account`, `escalation`). The aggregate curve (`psi_aggregate`) emphasizes primary semantic drift and is meant to relate to what you would trend on dashboards (distribution shift + anomaly rate), while still documenting label mix changes separately.

Across windows, PSI rises into the **investigation band** (>0.20) concurrent with sharper KS statistic trends on primary features (`ks_p_primary` becomes numerically negligible in late windows).

## Features Most Drifted
Primary drift dominates because simulated production traffic shifts upward in mean semantics (`+shift per window`). Secondary covariance drift emerges because correlated jitter noise increases concurrently (common when upstream logging changes subtly alter embeddings).

Separately, **intent label distributions drift materially** as technical share gradually declines while escalation-oriented traffic grows. This mirrors realistic production situations (product launches spike billing language; outages spike escalation language).

## Label Drift Interpretation (if labels were latent)
Because this subsystem is classification-oriented, latent label mixtures can shift faster than embeddings; **label PSI** captures this even when ground-truth supervision is delayed.

## Predicted Impact on Model Performance
For this support-intent system, escalation-heavy traffic is historically correlated with poorer automated resolution because intents require escalation workflows and nuanced policy interpretation.

Estimated downstream impact:

- At **aggregate PSI roughly 0.28–0.37** windows, expect **additional macro-F1 drop of roughly 4–8 points** versus reference week (narrower than benign weeks) assuming similar training methodology.
- SLA-resolution proxy KPI is expected to fall by **≈ 2–5 percentage points** because misroutes inflate manual review + rerouting time.
- **Escalation share growth** exacerbates SLA pressure because escalation paths consume higher human capacity per ticket.
- **Fairness slicing risk:** drift concentrated in `billing` vs `technical` imbalances can degrade routing precision for whichever segment becomes underrepresented in recent windows.

These ranges are plausible engineering priors anchored to classifier sensitivity curves; reproducible evidence plots are exported to `visualizations/drift_over_time.png` plus `visualizations/drift_summary.csv`.

## Recommended Interventions
- Trigger retraining when PSI > 0.20 for 3 consecutive windows.
- Add pre-processing normalization for new product-specific vocabulary.
- Expand monitoring slices by intent category and language style.
- Freeze model promotion if drift is increasing and A/B guardrails fail.

## How this ties back to monitoring
When drift climbs, operations should usually see correlated movement in gauges like `feature_drift_score` and higher `input_anomaly_rate`; error-rate spikes often follow prolonged drift if the classifier is stale. Prometheus alert stubs for these patterns are listed in `dashboards/prometheus-rules.yml`.
