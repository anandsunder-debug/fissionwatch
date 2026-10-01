"""Scenario runner for repeatable aerodynamic/trajectory studies."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
import numpy as np
from .flight_model import FlightParameters, FlightState, simulate

@dataclass(frozen=True)
class Scenario:
    name: str
    parameters: FlightParameters
    initial: FlightState
    times: np.ndarray
    force_model: Callable | None = None

def run_scenario(s: Scenario):
    return simulate(s.initial, s.parameters, s.times, s.force_model)

def run_suite(scenarios):
    return {s.name: run_scenario(s) for s in scenarios}
