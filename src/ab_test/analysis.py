"""Statistical helpers for A/B simulations."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass
class DifferenceTestResult:
    diff: float
    p_value: float
    ci_low: float
    ci_high: float


def proportions_two_sample_z(score_a: int, n_a: int, score_b: int, n_b: int, alpha: float = 0.05) -> DifferenceTestResult:
    """Explicit two-proportion z-test (+ Wald CI for the difference).

    Implemented with pooled-proportion SE for robustness vs equal proportions under H0,
    avoiding extra dependencies beyond scipy/numpy (course constraint friendly).
    """
    p_hat_a = score_a / n_a
    p_hat_b = score_b / n_b
    diff = float(p_hat_b - p_hat_a)

    pooled = float((score_a + score_b) / (n_a + n_b))
    se_pool = float(np.sqrt(pooled * (1 - pooled) * (1 / n_a + 1 / n_b)))
    z = diff / max(se_pool, 1e-12)
    p_value = float(2 * (1 - stats.norm.cdf(abs(z))))

    # Wald CI uses unpooled variance (common for inference on the difference itself)
    se_wald = float(np.sqrt(p_hat_a * (1 - p_hat_a) / n_a + p_hat_b * (1 - p_hat_b) / n_b))
    z_crit = float(stats.norm.ppf(1 - alpha / 2))
    return DifferenceTestResult(diff=diff, p_value=p_value, ci_low=diff - z_crit * se_wald, ci_high=diff + z_crit * se_wald)


def welch_mean_test(a_samples, b_samples, alpha: float = 0.05) -> DifferenceTestResult:
    a = np.asarray(a_samples, dtype=float)
    b = np.asarray(b_samples, dtype=float)

    mean_a = float(np.mean(a))
    mean_b = float(np.mean(b))

    _, p_value = stats.ttest_ind(b, a, equal_var=False)
    diff = mean_b - mean_a
    se = float(np.sqrt(np.var(a, ddof=1) / len(a) + np.var(b, ddof=1) / len(b)))
    z_crit = float(stats.norm.ppf(1 - alpha / 2))
    return DifferenceTestResult(diff=diff, p_value=float(p_value), ci_low=diff - z_crit * se, ci_high=diff + z_crit * se)
