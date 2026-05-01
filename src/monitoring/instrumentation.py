"""Prometheus instrumentation helpers for a prediction service."""

from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Dict

from prometheus_client import Counter, Gauge, Histogram, generate_latest

REQUEST_COUNT = Counter(
    "prediction_requests_total",
    "Total prediction requests",
    ["endpoint", "status"],
)
REQUEST_LATENCY = Histogram(
    "prediction_latency_seconds",
    "Prediction latency in seconds",
    ["endpoint"],
    buckets=(0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0),
)
ERROR_RATE = Gauge("prediction_error_rate", "Rolling error rate")
INPUT_ANOMALY_RATE = Gauge("input_anomaly_rate", "Invalid input ratio")
DRIFT_SCORE = Gauge("feature_drift_score", "Aggregated feature drift score")
THROUGHPUT = Gauge("prediction_throughput_rps", "Requests per second")


@dataclass
class RequestResult:
    endpoint: str
    latency_s: float
    status: str
    is_anomalous_input: bool


def process_request(endpoint: str = "/predict") -> RequestResult:
    """Simulate a request for local instrumentation testing."""
    start = time.perf_counter()
    simulated_work_s = random.uniform(0.01, 0.15)
    time.sleep(simulated_work_s)

    status = "error" if random.random() < 0.04 else "success"
    is_anomalous = random.random() < 0.03

    latency = time.perf_counter() - start
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
    REQUEST_COUNT.labels(endpoint=endpoint, status=status).inc()

    return RequestResult(
        endpoint=endpoint,
        latency_s=latency,
        status=status,
        is_anomalous_input=is_anomalous,
    )


def update_rolling_metrics(window: Dict[str, float]) -> None:
    ERROR_RATE.set(window.get("error_rate", 0.0))
    INPUT_ANOMALY_RATE.set(window.get("input_anomaly_rate", 0.0))
    DRIFT_SCORE.set(window.get("drift_score", 0.0))
    THROUGHPUT.set(window.get("throughput_rps", 0.0))


def export_metrics_text() -> str:
    return generate_latest().decode("utf-8")


if __name__ == "__main__":
    for _ in range(100):
        process_request()
    update_rolling_metrics(
        {
            "error_rate": 0.035,
            "input_anomaly_rate": 0.028,
            "drift_score": 0.19,
            "throughput_rps": 42.0,
        }
    )
    print(export_metrics_text())
