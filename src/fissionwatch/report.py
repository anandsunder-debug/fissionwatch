"""Reporting helpers."""

from __future__ import annotations

import re
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


def _mermaid_identifier(name: str, index: int) -> str:
    sanitized = re.sub(r"[^0-9A-Za-z_]", "_", name)
    if not sanitized or sanitized[0].isdigit():
        sanitized = f"node_{index}_{sanitized}"
    return sanitized


def _mermaid_label(name: str) -> str:
    return name.replace("\r", " ").replace("\n", "<br/>").replace('"', "&quot;")


def to_mermaid(graph: DependencyGraph) -> str:
    node_ids = {
        name: _mermaid_identifier(name, index)
        for index, name in enumerate(graph.graph.nodes)
    }
    lines = ["graph TD"]
    for source, target, data in graph.edges:
        lines.append(
            "    "
            f'{node_ids[source]}["{_mermaid_label(source)}"] -->|{float(data.get("coupling", 0.0)):.3f}| '
            f'{node_ids[target]}["{_mermaid_label(target)}"]'
        )
    return "\n".join(lines)
