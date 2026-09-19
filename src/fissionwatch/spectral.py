"""Spectral helpers for dependency graph analysis."""

from __future__ import annotations

import networkx as nx
import numpy as np

from .model import DependencyGraph


def _matrix(value: DependencyGraph | np.ndarray) -> np.ndarray:
    if isinstance(value, DependencyGraph):
        if value.graph.number_of_nodes() == 0:
            return np.zeros((0, 0))
        return nx.to_numpy_array(value.graph, weight="coupling", dtype=float)
    return np.asarray(value, dtype=float)


def spectral_radius(value: DependencyGraph | np.ndarray) -> float:
    matrix = _matrix(value)
    if matrix.size == 0:
        return 0.0
    return float(np.max(np.abs(np.linalg.eigvals(matrix))))


def modal_analysis(value: DependencyGraph | np.ndarray) -> dict[str, list[float] | float]:
    matrix = _matrix(value)
    if matrix.size == 0:
        return {"dominant_eigenvalue": 0.0, "eigenvalues": []}
    eigenvalues = np.linalg.eigvals(matrix)
    dominant = eigenvalues[np.argmax(np.abs(eigenvalues))]
    return {
        "dominant_eigenvalue": float(np.real_if_close(dominant).real),
        "eigenvalues": [float(np.real_if_close(v).real) for v in eigenvalues],
    }


def condition_report(value: DependencyGraph | np.ndarray) -> dict[str, float]:
    matrix = _matrix(value)
    if matrix.size == 0:
        return {"spectral_radius": 0.0, "condition_number": 0.0}
    return {
        "spectral_radius": spectral_radius(matrix),
        "condition_number": float(np.linalg.cond(matrix)),
    }


def edge_criticality_shares(graph: DependencyGraph) -> dict[str, float]:
    couplings = {
        f"{source}->{target}": float(data.get("coupling", 0.0))
        for source, target, data in graph.edges
    }
    total = sum(max(value, 0.0) for value in couplings.values())
    if total <= 0:
        return {key: 0.0 for key in couplings}
    return {key: value / total for key, value in couplings.items()}
