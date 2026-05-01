"""Feature drift and anomaly detection on synthetic windows."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp


def psi(expected: np.ndarray, actual: np.ndarray, bins: int = 10) -> float:
    breakpoints = np.quantile(expected, np.linspace(0, 1, bins + 1))
    breakpoints[0] = -np.inf
    breakpoints[-1] = np.inf

    expected_counts, _ = np.histogram(expected, bins=breakpoints)
    actual_counts, _ = np.histogram(actual, bins=breakpoints)

    expected_perc = np.clip(expected_counts / len(expected), 1e-6, None)
    actual_perc = np.clip(actual_counts / len(actual), 1e-6, None)

    return float(np.sum((actual_perc - expected_perc) * np.log(actual_perc / expected_perc)))

def categorical_psi(reference_labels: np.ndarray, production_labels: np.ndarray, categories: list[str]) -> float:
    ref_counts = {c: int(np.sum(reference_labels == c)) for c in categories}
    prod_counts = {c: int(np.sum(production_labels == c)) for c in categories}

    expected_perc = np.array([max(ref_counts[c] / len(reference_labels), 1e-9) for c in categories])
    actual_perc = np.array([max(prod_counts[c] / len(production_labels), 1e-9) for c in categories])

    return float(np.sum((actual_perc - expected_perc) * np.log(actual_perc / expected_perc)))


def generate_windows(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    reference_primary = rng.normal(0.0, 1.0, 1000)
    # Secondary feature as a mildly correlated jitter field (captures covariance shifts)
    reference_secondary = 0.35 * reference_primary + rng.normal(0.0, 0.6, size=1000)

    intents_ref = rng.choice(np.array(["billing", "technical", "account", "escalation"]), size=1200, p=np.array([0.35, 0.35, 0.20, 0.10]))

    for w in range(1, 13):
        shift = (w - 1) * 0.06
        primary_prod = rng.normal(shift, 1.05, 1000)
        secondary_noise = rng.normal((w - 1) * 0.02, 0.72, size=1000)
        secondary_prod = 0.35 * primary_prod + secondary_noise

        psi_primary = psi(reference_primary, primary_prod)
        psi_secondary = psi(reference_secondary, secondary_prod)

        ks_p_primary = ks_2samp(reference_primary, primary_prod).pvalue
        outlier_primary = float(np.mean(np.abs(primary_prod) > 3.0))

        # Label distribution drift simulation: slowly shift escalation share upward
        p = np.array([0.34, 0.33 - 0.008 * (w - 1), 0.20, 0.13 + 0.008 * (w - 1)])
        p = np.clip(p, 1e-3, None)
        p = p / p.sum()
        intents_prod = rng.choice(np.array(["billing", "technical", "account", "escalation"]), size=1200, p=p)

        intents = ["billing", "technical", "account", "escalation"]
        psi_label = categorical_psi(intents_ref, intents_prod, intents)

        # Aggregate PSI for alerting / dashboard coherence (weighted toward primary semantic signal)
        score = float(0.60 * psi_primary + 0.25 * psi_secondary + 0.15 * psi_label)

        ks_p = ks_p_primary

        rows.append((w, score, psi_primary, psi_secondary, psi_label, ks_p, outlier_primary))

    return pd.DataFrame(rows, columns=["window", "psi_aggregate", "psi_primary", "psi_secondary", "psi_labels", "ks_p_primary", "outlier_primary"])


def main() -> None:
    df = generate_windows()
    out_dir = Path("visualizations")
    out_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(1, 1, figsize=(9, 4.8))
    ax.plot(df["window"], df["psi_aggregate"], marker="o", label="PSI aggregate")
    ax.plot(df["window"], df["psi_primary"], marker="+", linestyle="--", alpha=0.8, label="PSI primary")
    ax.plot(df["window"], df["psi_secondary"], marker="x", linestyle=":", alpha=0.8, label="PSI secondary")
    ax.plot(df["window"], df["psi_labels"], marker=".", linestyle="-.", alpha=0.85, label="PSI label mix proxy")
    ax.axhline(0.2, linestyle="--", color="red", label="PSI threshold")
    ax.set_title("Feature + Label Distribution Drift (Windows)")
    ax.set_xlabel("Window")
    ax.set_ylabel("Score")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / "drift_over_time.png", dpi=200)

    df.to_csv(out_dir / "drift_summary.csv", index=False)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
