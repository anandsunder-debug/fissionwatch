"""Generic LBM field post-processing helpers."""
from __future__ import annotations
import numpy as np

def velocity_magnitude(ux, uy):
    return np.hypot(ux, uy)

def dynamic_pressure(rho, ux, uy):
    return 0.5 * np.asarray(rho) * (np.asarray(ux)**2 + np.asarray(uy)**2)

def field_summary(rho, ux, uy):
    speed = velocity_magnitude(ux, uy)
    return {"rho_min": float(np.min(rho)), "rho_max": float(np.max(rho)),
            "speed_mean": float(np.mean(speed)), "speed_max": float(np.max(speed))}
