import numpy as np
from src.simulation.geometry import profile_from_points
from src.simulation.flight_model import FlightParameters, FlightState, simulate

def test_profile_area_and_length():
    g = profile_from_points([(0.0,0.01),(0.1,0.02),(0.2,0.01)])
    assert np.isclose(g.length, 0.2)
    assert np.isclose(g.area_at(0.1), np.pi * 0.02**2)

def test_zero_external_force_has_gravity():
    p = FlightParameters(mass=1.0, inertia=1.0, area=0.0)
    t = np.linspace(0,1,11)
    y = simulate(FlightState(), p, t)
    assert y[-1,1] < 0
    assert np.isclose(y[-1,3], -9.81, atol=1e-6)
