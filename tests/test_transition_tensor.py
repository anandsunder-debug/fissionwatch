import numpy as np
from sai_core import Entity, Transition, StructuralAdaptiveTensor


def test_tensor_shape_and_ingest():
    model = StructuralAdaptiveTensor([Entity("a", "query"), Entity("b", "index")], ["uses"])
    model.ingest([Transition(0, 1, 0, weight=2.0)])
    assert model.conductance.shape == (2, 2, 1)
    assert model.conductance[0, 1, 0] == 2.0


def test_distribution_normalizes():
    model = StructuralAdaptiveTensor([Entity("a", "query"), Entity("b", "index")], ["uses"])
    model.ingest([Transition(0, 1, 0, weight=2.0)])
    distribution = model.transition_distribution(0, 0)
    assert np.isclose(distribution.sum(), 1.0)
    assert np.isclose(distribution[1], 1.0)


def test_adaptation_reinforces_observation():
    model = StructuralAdaptiveTensor([Entity("a", "query"), Entity("b", "index")], ["uses"])
    model.ingest([Transition(0, 1, 0, weight=1.0)])
    before = model.conductance[0, 1, 0]
    model.adapt([Transition(0, 1, 0, weight=2.0, cost=1.0)])
    assert model.conductance[0, 1, 0] > before
