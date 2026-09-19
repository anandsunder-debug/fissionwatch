import unittest
from unittest.mock import patch

from fissionwatch.model import EdgeKind
from fissionwatch.telemetry.scrape import (
    EdgeTelemetry,
    TelemetryMapping,
    graph_from_prometheus,
)


class TelemetryTests(unittest.TestCase):
    def test_error_ratio_is_safe(self):
        self.assertEqual(EdgeTelemetry("a", "b", errors_per_second=2, calls_per_second=4).error_ratio, 0.5)
        self.assertEqual(EdgeTelemetry("a", "b").error_ratio, 0.0)

    def test_mapping_is_configurable(self):
        mapping = TelemetryMapping(source_label="caller", target_label="callee", query_window="1m")
        self.assertEqual(mapping.source_label, "caller")
        self.assertEqual(mapping.query_window, "1m")

    @patch("fissionwatch.telemetry.scrape.collect_edge_telemetry")
    def test_graph_from_prometheus_builds_dependency_graph(self, collect_edge_telemetry):
        collect_edge_telemetry.return_value = [
            EdgeTelemetry("checkout", "payments", calls_per_second=10, errors_per_second=2, latency_seconds=0.3)
        ]

        graph = graph_from_prometheus("https://prometheus.example.com")
        source, target, data = next(iter(graph.edges))

        self.assertEqual((source, target), ("checkout", "payments"))
        self.assertEqual(data["kind"], EdgeKind.CALL)
        self.assertAlmostEqual(data["coupling"], 0.2)
        self.assertAlmostEqual(data["latency_s"], 0.3)


if __name__ == "__main__":
    unittest.main()
