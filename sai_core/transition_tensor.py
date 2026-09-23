"""Knowledge-representation and tensor model for Structural Adaptive Intelligence.

This module intentionally uses no neurons, neural networks, or gradient training.
It represents entities, relations, observations, and transitions as tensors and
updates edge conductance using a Physarum-inspired positive-feedback rule.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence
import numpy as np


@dataclass(frozen=True)
class Entity:
    entity_id: str
    kind: str


@dataclass(frozen=True)
class Transition:
    source: int
    target: int
    relation: int
    weight: float = 1.0
    cost: float = 1.0


class StructuralAdaptiveTensor:
    """Symbolic knowledge graph with a dynamic transition/conductance tensor.

    Tensor shape: [source_entity, target_entity, relation_type].
    Values represent adaptive conductance, not learned neural weights.
    """

    def __init__(self, entities: Sequence[Entity], relation_types: Sequence[str],
                 evaporation: float = 0.08, reinforcement: float = 0.25,
                 minimum_conductance: float = 1e-4):
        if not 0 <= evaporation < 1:
            raise ValueError("evaporation must be in [0, 1)")
        self.entities = tuple(entities)
        self.relation_types = tuple(relation_types)
        n, r = len(self.entities), len(self.relation_types)
        self.conductance = np.zeros((n, n, r), dtype=float)
        self.evidence = np.zeros_like(self.conductance)
        self.evaporation = evaporation
        self.reinforcement = reinforcement
        self.minimum_conductance = minimum_conductance

    def ingest(self, transitions: Iterable[Transition]) -> None:
        for item in transitions:
            self._validate(item)
            self.conductance[item.source, item.target, item.relation] += max(item.weight, 0.0)
            self.evidence[item.source, item.target, item.relation] += 1.0

    def adapt(self, observed: Iterable[Transition]) -> None:
        """Apply evaporation plus evidence-driven reinforcement."""
        self.conductance *= (1.0 - self.evaporation)
        for item in observed:
            self._validate(item)
            s = max(item.source, 0)
            t = max(item.target, 0)
            r = max(item.relation, 0)
            support = max(item.weight, 0.0) / max(item.cost, 1e-9)
            self.conductance[s, t, r] += self.reinforcement * support
            self.evidence[s, t, r] += 1.0
        self.conductance[self.conductance < self.minimum_conductance] = 0.0

    def transition_distribution(self, source: int, relation: int) -> np.ndarray:
        """Return normalized outgoing transition probabilities."""
        scores = self.conductance[source, :, relation].copy()
        total = scores.sum()
        return scores / total if total > 0 else np.zeros_like(scores)

    def strongest_transitions(self, limit: int = 10) -> list[tuple[int, int, int, float]]:
        indices = np.argwhere(self.conductance > 0)
        ranked = sorted(
            ((int(s), int(t), int(r), float(self.conductance[s, t, r])) for s, t, r in indices),
            key=lambda x: x[3], reverse=True,
        )
        return ranked[:limit]

    def _validate(self, item: Transition) -> None:
        n, r = len(self.entities), len(self.relation_types)
        if not (0 <= item.source < n and 0 <= item.target < n):
            raise IndexError("entity index outside tensor bounds")
        if not 0 <= item.relation < r:
            raise IndexError("relation index outside tensor bounds")
        if item.cost <= 0:
            raise ValueError("transition cost must be positive")
