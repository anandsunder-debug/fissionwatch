"""fissionwatch public package interface."""

from ._version import __version__
from .analyzer import AnalyzerConfig, FissionAnalyzer, FissionReport, Mitigation, apply_mitigation
from .cascade import classify_regime, failure_wave, rf_series, simulate_cascade
from .customer import (
    CustomerReliabilitySnapshot,
    capacity_adjusted_sri,
    capacity_margin,
    customer_experience_quality,
    customer_impact_amplification,
    customer_reliability,
    customer_trust_index,
    recovery_elasticity,
    reliability_adjusted_sri,
    spectral_resilience,
    trust_stability,
)
from .detectors import Finding
from .model import Dependency, DependencyGraph, EdgeKind, Node, Trust, Vulnerability
from .report import markdown, to_mermaid
from .spectral import condition_report, edge_criticality_shares, modal_analysis, spectral_radius
from .telemetry import (
    EdgeTelemetry,
    TelemetryMapping,
    collect_edge_telemetry,
    graph_from_prometheus,
    scrape_prometheus,
)

__all__ = [
    "__version__",
    "AnalyzerConfig",
    "CustomerReliabilitySnapshot",
    "Dependency",
    "DependencyGraph",
    "EdgeKind",
    "EdgeTelemetry",
    "Finding",
    "FissionAnalyzer",
    "FissionReport",
    "Mitigation",
    "Node",
    "TelemetryMapping",
    "Trust",
    "Vulnerability",
    "apply_mitigation",
    "capacity_adjusted_sri",
    "capacity_margin",
    "classify_regime",
    "collect_edge_telemetry",
    "condition_report",
    "customer_experience_quality",
    "customer_impact_amplification",
    "customer_reliability",
    "customer_trust_index",
    "edge_criticality_shares",
    "failure_wave",
    "graph_from_prometheus",
    "markdown",
    "modal_analysis",
    "recovery_elasticity",
    "reliability_adjusted_sri",
    "rf_series",
    "scrape_prometheus",
    "simulate_cascade",
    "spectral_resilience",
    "spectral_radius",
    "to_mermaid",
    "trust_stability",
]
