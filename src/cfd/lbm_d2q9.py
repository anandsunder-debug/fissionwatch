"""Generic D2Q9 BGK lattice-Boltzmann utilities.

Reusable numerical core extracted from the uploaded CFD project.
No vehicle, propulsion, combustion, or rocket-specific geometry is included.
"""

from __future__ import annotations
import numpy as np

C = np.array([[0,0],[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,1],[-1,-1],[1,-1]], dtype=int)
W = np.array([4/9,1/9,1/9,1/9,1/9,1/36,1/36,1/36,1/36], dtype=float)
OPP = np.array([0,3,4,1,2,7,8,5,6], dtype=int)

def equilibrium(rho: np.ndarray, ux: np.ndarray, uy: np.ndarray) -> np.ndarray:
    """Return D2Q9 equilibrium populations with shape (9, ny, nx)."""
    cu = 3.0 * (C[:,0,None,None] * ux + C[:,1,None,None] * uy)
    u2 = 1.5 * (ux*ux + uy*uy)
    return W[:,None,None] * rho[None,:,:] * (1.0 + cu + 0.5*cu*cu - u2[None,:,:])

def macroscopic(f: np.ndarray) -> tuple[np.ndarray,np.ndarray,np.ndarray]:
    """Recover density and velocity from populations."""
    rho = f.sum(axis=0)
    ux = (f * C[:,0,None,None]).sum(axis=0) / np.maximum(rho, 1e-12)
    uy = (f * C[:,1,None,None]).sum(axis=0) / np.maximum(rho, 1e-12)
    return rho, ux, uy

def collide_bgk(f: np.ndarray, tau: float) -> np.ndarray:
    """BGK collision step."""
    rho, ux, uy = macroscopic(f)
    feq = equilibrium(rho, ux, uy)
    return f + (feq - f) / tau

def stream(f: np.ndarray) -> np.ndarray:
    """Periodic streaming; apply physical boundaries after this operation."""
    out = np.empty_like(f)
    for q, (cx, cy) in enumerate(C):
        out[q] = np.roll(np.roll(f[q], cy, axis=0), cx, axis=1)
    return out

def bounce_back(f: np.ndarray, solid: np.ndarray) -> np.ndarray:
    """Half-way bounce-back for a boolean solid mask."""
    out = f.copy()
    for q in range(1, 9):
        out[q, solid] = f[OPP[q], solid]
    return out

def initialize(nx: int, ny: int, rho0: float = 1.0, ux0: float = 0.0, uy0: float = 0.0) -> np.ndarray:
    """Initialize an equilibrium field."""
    rho = np.full((ny,nx), rho0, dtype=float)
    ux = np.full((ny,nx), ux0, dtype=float)
    uy = np.full((ny,nx), uy0, dtype=float)
    return equilibrium(rho, ux, uy)
