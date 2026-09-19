"""Minimal dependency graph model used by telemetry ingestion."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import networkx as nx


class EdgeKind(str, Enum):
    """Supported dependency edge kinds."""

    CALL = "call"


@dataclass(frozen=True)
class Dependency:
    """A directed dependency edge between two services."""

    source: str
    target: str
    coupling: float = 0.0
    latency_s: float = 0.0
    retries: int = 0
    kind: EdgeKind = EdgeKind.CALL


class DependencyGraph:
    """Small wrapper around a directed dependency graph."""

    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def add_dependency(
        self,
        source: str,
        target: str,
        *,
        coupling: float = 0.0,
        latency_s: float = 0.0,
        retries: int = 0,
        kind: EdgeKind = EdgeKind.CALL,
    ) -> None:
        self.graph.add_edge(
            source,
            target,
            coupling=float(coupling),
            latency_s=float(latency_s),
            retries=int(retries),
            kind=kind,
        )

    @property
    def edges(self):
        return self.graph.edges(data=True)
