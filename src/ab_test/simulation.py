"""A/B test simulation with power-aware sample size."""

from __future__ import annotations

import argparse

import numpy as np
from scipy import stats


def required_sample_size(std: float, mde: float, alpha: float = 0.05, power: float = 0.8) -> int:
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    n = 2 * ((z_alpha + z_beta) * std / mde) ** 2
    return int(np.ceil(n))


def simulate(seed: int = 7, n: int = 2000) -> None:
    from analysis import proportions_two_sample_z, welch_mean_test

    rng = np.random.default_rng(seed)

    # KPI 1 (primary/Bernoulli): SLA-resolution rate (within SLA routing window)
    a_sla_success = rng.binomial(1, 0.62, size=n)
    b_sla_success = rng.binomial(1, 0.66, size=n)

    # KPI 2 (Bernoulli): escalation due to unclear intent / downstream failure
    a_esc = rng.binomial(1, 0.11, size=n)
    b_esc = rng.binomial(1, 0.09, size=n)

    # KPI 3 (Bernoulli): groundedness proxy (human audit pass)
    a_ground = rng.binomial(1, 0.78, size=n)
    b_ground = rng.binomial(1, 0.82, size=n)

    # KPI 4 (continuous): latency (minutes)
    latency_a_sec = rng.gamma(shape=9.0, scale=1.0 / 40.0, size=n)
    latency_b_sec = rng.gamma(shape=9.0, scale=1.0 / 46.0, size=n)

    def summarize_prop(a_bits, b_bits):
        ma = float(np.mean(a_bits))
        mb = float(np.mean(b_bits))
        scored_a = int(np.sum(a_bits))
        scored_b = int(np.sum(b_bits))
        res = proportions_two_sample_z(scored_a, n, scored_b, n)
        return ma, mb, res

    sla_a, sla_b, sla_res = summarize_prop(a_sla_success, b_sla_success)
    esc_a, esc_b, esc_res = summarize_prop(a_esc, b_esc)
    gr_a, gr_b, gr_res = summarize_prop(a_ground, b_ground)
    lat_res = welch_mean_test(latency_a_sec, latency_b_sec)

    print("-- Primary KPI --")
    print(f"sla_resolution_rate_a={sla_a:.4f}")
    print(f"sla_resolution_rate_b={sla_b:.4f}")
    print(f"uplift_pct_vs_A={(sla_b-sla_a)/max(sla_a,1e-9)*100:.2f}")
    print(f"ztest_p_value={sla_res.p_value:.6f}")
    print(f"effect_diff_CI95=[{sla_res.ci_low:.4f},{sla_res.ci_high:.4f}]")

    print("-- Guardrail / secondary KPIs --")
    print(f"escalation_rate_a={esc_a:.4f} escalation_rate_b={esc_b:.4f} p={esc_res.p_value:.6f}")
    print(f"groundedness_proxy_a={gr_a:.4f} groundedness_proxy_b={gr_b:.4f} p={gr_res.p_value:.6f}")
    print(
        "latency_mean_sec="
        + f"a={float(np.mean(latency_a_sec)):.4f} b={float(np.mean(latency_b_sec)):.4f} "
        + f"p={lat_res.p_value:.6f} "
        + f"ci_diff_sec=[{lat_res.ci_low:.4f},{lat_res.ci_high:.4f}]"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    n_required = required_sample_size(std=0.48, mde=0.03)
    n = max(2000, n_required)
    print(f"required_n_per_variant={n_required}")
    print(f"simulate_n_per_variant={n}")
    simulate(n=n)

    if args.dry_run:
        print("dry_run_ok=true")


if __name__ == "__main__":
    main()
