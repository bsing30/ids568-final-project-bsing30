"""Generate synthetic request traffic and monitoring snapshots."""

from __future__ import annotations

from pathlib import Path
import os
import random
import threading

import matplotlib.pyplot as plt
import numpy as np

from instrumentation import process_request, update_rolling_metrics


def run_simulation(n: int = 600) -> None:
    latencies = []
    error_flags = []
    anomaly_flags = []
    drift = []

    for i in range(n):
        result = process_request()
        latencies.append(result.latency_s * 1000)
        error_flags.append(1 if result.status == "error" else 0)
        anomaly_flags.append(1 if result.is_anomalous_input else 0)

        drift_score = max(0.0, min(1.0, 0.08 + 0.00035 * i + random.uniform(-0.02, 0.02)))
        drift.append(drift_score)

        if (i + 1) % 30 == 0:
            window_slice = slice(max(0, i - 29), i + 1)
            window = {
                "error_rate": float(np.mean(error_flags[window_slice])),
                "input_anomaly_rate": float(np.mean(anomaly_flags[window_slice])),
                "drift_score": float(np.mean(drift[window_slice])),
                "throughput_rps": 20.0 + random.uniform(-2.0, 4.0),
            }
            update_rolling_metrics(window)

    out = Path("visualizations")
    out.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(12, 7))
    x = np.arange(n)

    axes[0, 0].plot(x, latencies, color="#1f77b4")
    axes[0, 0].set_title("Latency (ms)")
    axes[0, 0].set_ylabel("ms")

    rolling_error = np.convolve(error_flags, np.ones(30) / 30, mode="same")
    axes[0, 1].plot(x, rolling_error * 100, color="#d62728")
    axes[0, 1].set_title("Rolling Error Rate (%)")

    rolling_anomaly = np.convolve(anomaly_flags, np.ones(30) / 30, mode="same")
    axes[1, 0].plot(x, rolling_anomaly * 100, color="#ff7f0e")
    axes[1, 0].set_title("Input Integrity Anomaly Rate (%)")
    axes[1, 0].set_xlabel("Request index")

    axes[1, 1].plot(x, drift, color="#2ca02c")
    axes[1, 1].axhline(0.25, linestyle="--", color="black", label="Alert threshold")
    axes[1, 1].set_title("Feature Drift Score")
    axes[1, 1].set_xlabel("Request index")
    axes[1, 1].legend()

    fig.tight_layout()
    fig.savefig(out / "dashboard-screenshot.png", dpi=200)


if __name__ == "__main__":
    metrics_port_raw = os.environ.get("METRICS_SERVE_PORT", "").strip()
    if metrics_port_raw:
        metrics_port = int(metrics_port_raw)
        # Imported here so this script stays runnable without import cycles when used as __main__.
        from metrics_exporter import serve as serve_metrics

        threading.Thread(
            target=serve_metrics,
            kwargs={"host": "127.0.0.1", "port": metrics_port},
            daemon=True,
        ).start()
    run_simulation()
