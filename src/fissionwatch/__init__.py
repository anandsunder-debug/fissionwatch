"""fissionwatch - detect and monitor software chain reactions (fission modes) in dependency graphs.

Implements and extends the thresholded branching-and-propagation model of
"Experimental Evidence for Software Fission" (Sunder): R_f, rho(J), critical margin,
blast radius, failure-wave propagation, spectral conditioning of K.
"""
from .analyzer import AnalyzerConfig, FissionAnalyzer, FissionReport, Mitigation, apply_mitigation
from .cascade import classify_regime, failure_wave, rf_series, simulate_cascade
from .detectors import Finding
from .model import Dependency, DependencyGraph, EdgeKind, Node, Trust, Vulnerability
from .report import markdown, to_mermaid
from .spectral import condition_report, edge_criticality_shares, modal_analysis, spectral_radius
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

__version__ = "0.1.1"
__all__ = ["AnalyzerConfig", "FissionAnalyzer", "FissionReport", "Mitigation", "apply_mitigation",
           "classify_regime", "failure_wave", "rf_series", "simulate_cascade", "Finding", "Dependency",
           "DependencyGraph", "EdgeKind", "Node", "Trust", "Vulnerability", "markdown", "to_mermaid",
           "condition_report", "edge_criticality_shares", "modal_analysis", "spectral_radius",
           "CustomerReliabilitySnapshot", "capacity_adjusted_sri", "capacity_margin",
           "customer_experience_quality", "customer_impact_amplification", "customer_reliability",
           "customer_trust_index", "recovery_elasticity", "reliability_adjusted_sri",
           "spectral_resilience", "trust_stability"]
