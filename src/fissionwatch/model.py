"""Dependency graph model types used across the package."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import networkx as nx


class Trust(str, Enum):
    """Coarse trust level annotations for a node."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    UNKNOWN = "unknown"


class EdgeKind(str, Enum):
    """Supported dependency edge kinds."""

    CALL = "call"
    DATA = "data"
    CONTROL = "control"


@dataclass(frozen=True)
class Node:
    """A service or subsystem in the dependency graph."""

    name: str
    trust: Trust = Trust.UNKNOWN


@dataclass(frozen=True)
class Vulnerability:
    """A lightweight vulnerability annotation."""

    identifier: str
    severity: float = 0.0


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

    def add_node(self, node: str | Node, **attributes) -> None:
        if isinstance(node, Node):
            self.graph.add_node(node.name, trust=node.trust.value, **attributes)
            return
        self.graph.add_node(node, **attributes)

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

    def copy(self) -> "DependencyGraph":
        duplicate = DependencyGraph()
        duplicate.graph = self.graph.copy()
        return duplicate
