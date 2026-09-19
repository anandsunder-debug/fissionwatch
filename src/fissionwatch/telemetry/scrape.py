"""Generic telemetry ingestion from Prometheus-compatible endpoints.

The adapter intentionally depends only on the Python standard library. It can
consume metrics from Prometheus, VictoriaMetrics, Thanos, Grafana Mimir, or an
OpenTelemetry Collector Prometheus exporter. Metric names and labels are
configurable so it is not tied to a particular enterprise stack.
"""
from __future__ import annotations

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Any

from ..model import DependencyGraph, EdgeKind


@dataclass
class TelemetryMapping:
    """Map enterprise metric conventions to normalized edge telemetry."""
    source_label: str = "source"
    target_label: str = "destination"
    request_metric: str = "http_requests_total"
    error_metric: str = "http_requests_total"
    latency_metric: str = "http_request_duration_seconds_sum"
    saturation_metric: str | None = None
    retry_metric: str | None = None
    error_label: str = "status"
    error_regex: str = "5.."
    latency_count_metric: str = "http_request_duration_seconds_count"
    query_window: str = "5m"


@dataclass
class EdgeTelemetry:
    source: str
    target: str
    calls_per_second: float = 0.0
    errors_per_second: float = 0.0
    latency_seconds: float = 0.0
    saturation: float = 0.0
    retries_per_second: float = 0.0
    labels: dict[str, str] = field(default_factory=dict)

    @property
    def error_ratio(self) -> float:
        return self.errors_per_second / max(self.calls_per_second, 1e-9)


def scrape_prometheus(base_url: str, query: str, timeout_s: float = 10.0) -> list[dict[str, Any]]:
    """Execute a PromQL instant query and return vector samples."""
    url = base_url.rstrip("/") + "/api/v1/query?" + urllib.parse.urlencode({"query": query})
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout_s) as response:  # nosec B310
        payload = json.loads(response.read().decode("utf-8"))
    if payload.get("status") != "success":
        raise RuntimeError(f"Prometheus query failed: {payload.get('error', payload)}")
    return payload.get("data", {}).get("result", [])


def _value(sample: dict[str, Any]) -> float:
    try:
        return float(sample.get("value", [0, 0])[1])
    except (TypeError, ValueError, IndexError):
        return 0.0


def _index(samples: list[dict[str, Any]], mapping: TelemetryMapping) -> dict[tuple[str, str], float]:
    out: dict[tuple[str, str], float] = {}
    for sample in samples:
        labels = sample.get("metric", {})
        source, target = labels.get(mapping.source_label), labels.get(mapping.target_label)
        if source and target:
            out[(source, target)] = out.get((source, target), 0.0) + _value(sample)
    return out


def collect_edge_telemetry(base_url: str, mapping: TelemetryMapping | None = None,
                           timeout_s: float = 10.0) -> list[EdgeTelemetry]:
    """Pull normalized edge metrics using configurable PromQL templates."""
    m = mapping or TelemetryMapping()
    q = lambda metric: f"sum by ({m.source_label},{m.target_label}) (rate({metric}[{m.query_window}]))"
    calls = _index(scrape_prometheus(base_url, q(m.request_metric), timeout_s), m)
    errors = _index(scrape_prometheus(base_url,
        f'sum by ({m.source_label},{m.target_label}) (rate({m.error_metric}{{{m.error_label}=~"{m.error_regex}"}}[{m.query_window}]))', timeout_s), m)
    latency_sum = _index(scrape_prometheus(base_url, q(m.latency_metric), timeout_s), m)
    latency_count = _index(scrape_prometheus(base_url, q(m.latency_count_metric), timeout_s), m)
    retries = _index(scrape_prometheus(base_url, q(m.retry_metric), timeout_s), m) if m.retry_metric else {}
    saturation = _index(scrape_prometheus(base_url, q(m.saturation_metric), timeout_s), m) if m.saturation_metric else {}
    keys = set(calls) | set(errors) | set(latency_sum) | set(latency_count) | set(retries) | set(saturation)
    return [EdgeTelemetry(a, b, calls.get((a, b), 0.0), errors.get((a, b), 0.0),
                          latency_sum.get((a, b), 0.0) / max(latency_count.get((a, b), 0.0), 1e-9),
                          saturation.get((a, b), 0.0), retries.get((a, b), 0.0)) for a, b in sorted(keys)]


def graph_from_prometheus(base_url: str, mapping: TelemetryMapping | None = None,
                          timeout_s: float = 10.0) -> DependencyGraph:
    """Build a DependencyGraph from live edge telemetry."""
    graph = DependencyGraph()
    for e in collect_edge_telemetry(base_url, mapping, timeout_s):
        coupling = min(1.0, max(e.error_ratio, e.saturation * 0.5))
        graph.add_dependency(e.source, e.target, coupling=coupling,
                             latency_s=e.latency_seconds, retries=round(e.retries_per_second),
                             kind=EdgeKind.CALL)
    return graph
