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

__version__ = "0.1.0"
__all__ = ["AnalyzerConfig", "FissionAnalyzer", "FissionReport", "Mitigation", "apply_mitigation",
           "classify_regime", "failure_wave", "rf_series", "simulate_cascade", "Finding", "Dependency",
           "DependencyGraph", "EdgeKind", "Node", "Trust", "Vulnerability", "markdown", "to_mermaid",
           "condition_report", "edge_criticality_shares", "modal_analysis", "spectral_radius"]
