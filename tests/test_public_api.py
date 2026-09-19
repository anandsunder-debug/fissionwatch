import unittest

from fissionwatch import (
    AnalyzerConfig,
    Dependency,
    DependencyGraph,
    EdgeKind,
    Finding,
    FissionAnalyzer,
    FissionReport,
    Mitigation,
    Node,
    Trust,
    Vulnerability,
    apply_mitigation,
    classify_regime,
    condition_report,
    edge_criticality_shares,
    failure_wave,
    markdown,
    modal_analysis,
    rf_series,
    simulate_cascade,
    spectral_radius,
    to_mermaid,
)


class PublicApiTests(unittest.TestCase):
    def test_public_symbols_are_importable(self):
        graph = DependencyGraph()
        graph.add_node(Node("checkout", trust=Trust.HIGH))
        graph.add_dependency("checkout", "payments", coupling=0.4, kind=EdgeKind.CALL)

        self.assertIsInstance(AnalyzerConfig(), AnalyzerConfig)
        self.assertIsInstance(Dependency("checkout", "payments"), Dependency)
        self.assertIsInstance(Finding("rule", "message"), Finding)
        self.assertIsInstance(FissionAnalyzer().analyze(graph), FissionReport)
        self.assertIsInstance(Mitigation("checkout", "payments"), Mitigation)
        self.assertIsInstance(Vulnerability("CVE-2026-0001"), Vulnerability)
        self.assertEqual(classify_regime(0.5), "subcritical")
        self.assertIsInstance(condition_report(graph), dict)
        self.assertIsInstance(edge_criticality_shares(graph), dict)
        self.assertIsInstance(failure_wave(graph), list)
        self.assertIn("# Fission Report", markdown(FissionAnalyzer().analyze(graph)))
        self.assertIsInstance(modal_analysis(graph), dict)
        self.assertIsInstance(rf_series(graph), list)
        self.assertIsInstance(simulate_cascade(graph, ["checkout"]), list)
        self.assertGreaterEqual(spectral_radius(graph), 0.0)
        self.assertIn("graph TD", to_mermaid(graph))
        mitigated = apply_mitigation(graph, Mitigation("checkout", "payments", coupling_scale=0.5))
        _, _, data = next(iter(mitigated.edges))
        self.assertAlmostEqual(data["coupling"], 0.2)


if __name__ == "__main__":
    unittest.main()
