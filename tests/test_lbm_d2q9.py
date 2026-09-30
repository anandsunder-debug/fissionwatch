import numpy as np
from src.cfd.lbm_d2q9 import initialize, macroscopic, equilibrium, collide_bgk

def test_equilibrium_recovers_uniform_state():
    f = initialize(12, 8, rho0=1.0, ux0=0.02, uy0=-0.01)
    rho, ux, uy = macroscopic(f)
    assert np.allclose(rho, 1.0)
    assert np.allclose(ux, 0.02)
    assert np.allclose(uy, -0.01)

def test_collision_preserves_equilibrium():
    f = initialize(10, 10, rho0=1.0, ux0=0.01, uy0=0.0)
    out = collide_bgk(f, tau=0.8)
    assert np.allclose(out, f)
