"""Generic axisymmetric geometry helpers.

The module represents a computational test article as a radius-vs-axis profile.
It intentionally contains no fabrication, nozzle, propellant, or combustion logic.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class BodyProfile:
    x: np.ndarray
    radius: np.ndarray
    def __post_init__(self):
        if self.x.ndim != 1 or self.radius.ndim != 1 or len(self.x) != len(self.radius):
            raise ValueError("x and radius must be one-dimensional arrays of equal length")
        if len(self.x) < 2 or np.any(np.diff(self.x) <= 0):
            raise ValueError("x must contain at least two strictly increasing points")
        if np.any(self.radius <= 0):
            raise ValueError("radius must be positive")
    @property
    def length(self) -> float:
        return float(self.x[-1] - self.x[0])
    def radius_at(self, xq):
        return np.interp(xq, self.x, self.radius)
    def area_at(self, xq):
        return np.pi * self.radius_at(xq) ** 2
    def reference_area(self) -> float:
        return float(np.pi * np.max(self.radius) ** 2)

def profile_from_points(points):
    arr=np.asarray(points,dtype=float)
    if arr.ndim != 2 or arr.shape[1] != 2:
        raise ValueError("points must have shape (N, 2)")
    return BodyProfile(arr[:,0],arr[:,1])
