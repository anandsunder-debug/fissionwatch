"""Cascade simulation helpers."""

from __future__ import annotations

from collections.abc import Iterable

import networkx as nx
import numpy as np

from .model import DependencyGraph
from .spectral import spectral_radius


def _matrix(graph: DependencyGraph) -> np.ndarray:
    if graph.graph.number_of_nodes() == 0:
        return np.zeros((0, 0))
    return nx.to_numpy_array(graph.graph, weight="coupling", dtype=float)


def rf_series(graph: DependencyGraph, steps: int = 5) -> list[float]:
    matrix = _matrix(graph)
    if matrix.size == 0:
        return []
    scale = spectral_radius(matrix)
    return [float(scale ** step) for step in range(1, steps + 1)]


def failure_wave(graph: DependencyGraph, steps: int = 5) -> list[float]:
    series = [0.0] + rf_series(graph, steps=steps)
    return [series[index + 1] - series[index] for index in range(len(series) - 1)]


def classify_regime(value: float, critical_tolerance: float = 0.05) -> str:
    if value < 1.0 - critical_tolerance:
        return "subcritical"
    if value > 1.0 + critical_tolerance:
        return "supercritical"
    return "critical"


def simulate_cascade(
    graph: DependencyGraph,
    initial_failures: Iterable[str],
    threshold: float = 0.5,
    max_steps: int = 10,
) -> list[set[str]]:
    failed = set(initial_failures)
    waves = [set(failed)]
    for _ in range(max_steps):
        new_failures: set[str] = set()
        for source, target, data in graph.edges:
            if source in failed and float(data.get("coupling", 0.0)) >= threshold and target not in failed:
                new_failures.add(target)
        if not new_failures:
            break
        failed.update(new_failures)
        waves.append(new_failures)
    return waves
