"""Reporting helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .model import DependencyGraph

if TYPE_CHECKING:
    from .analyzer import FissionReport


def markdown(report: FissionReport) -> str:
    return "\n".join(
        [
            "# Fission Report",
            f"- Spectral radius: {report.spectral_radius:.6f}",
            f"- Regime: {report.regime}",
            f"- Failure wave: {', '.join(f'{value:.6f}' for value in report.failure_wave) or 'n/a'}",
        ]
    )


def to_mermaid(graph: DependencyGraph) -> str:
    lines = ["graph TD"]
    for source, target, data in graph.edges:
        lines.append(f"    {source} -->|{float(data.get('coupling', 0.0)):.3f}| {target}")
    return "\n".join(lines)
