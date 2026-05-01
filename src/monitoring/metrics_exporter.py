"""Optional mini endpoint to expose Prometheus text metrics (:8000/metrics).

This complements `instrumentation.py` by exporting the same gauges/counters/histograms
during local simulations/demos without requiring Prometheus to scrape gauges from logs.
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import generate_latest


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args):  # noqa: A003
        return

    def do_GET(self):  # noqa: N802
        if self.path == "/metrics":
            payload = generate_latest()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4; charset=utf-8")
            self.end_headers()
            self.wfile.write(payload)
            return
        if self.path in {"/healthz", "/"}:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
            return
        self.send_error(404)


def serve(host: str = "0.0.0.0", port: int = 8000) -> None:
    httpd = HTTPServer((host, port), _Handler)
    httpd.serve_forever()


if __name__ == "__main__":
    serve()
