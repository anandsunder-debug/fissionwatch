"""High-level analysis helpers."""

from __future__ import annotations

from dataclasses import dataclass, field

from .cascade import classify_regime, failure_wave
from .model import DependencyGraph
from .spectral import edge_criticality_shares, spectral_radius


@dataclass(frozen=True)
class AnalyzerConfig:
    wave_steps: int = 5


@dataclass(frozen=True)
class Mitigation:
    source: str
    target: str
    coupling_scale: float = 1.0


@dataclass(frozen=True)
class FissionReport:
    spectral_radius: float
    regime: str
    failure_wave: list[float] = field(default_factory=list)
    edge_criticality: dict[str, float] = field(default_factory=dict)


class FissionAnalyzer:
    def __init__(self, config: AnalyzerConfig | None = None) -> None:
        self.config = config or AnalyzerConfig()

    def analyze(self, graph: DependencyGraph) -> FissionReport:
        rho = spectral_radius(graph)
        return FissionReport(
            spectral_radius=rho,
            regime=classify_regime(rho),
            failure_wave=failure_wave(graph, steps=self.config.wave_steps),
            edge_criticality=edge_criticality_shares(graph),
        )


def apply_mitigation(graph: DependencyGraph, mitigation: Mitigation) -> DependencyGraph:
    updated = graph.copy()
    if updated.graph.has_edge(mitigation.source, mitigation.target):
        edge = updated.graph[mitigation.source][mitigation.target]
        edge["coupling"] = float(edge.get("coupling", 0.0)) * float(mitigation.coupling_scale)
    return updated
