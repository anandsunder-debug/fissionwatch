"""Customer-aware flow--structural reliability metrics from Sunder (2026).

The implementation is intentionally transparent and experimental: model inputs are
normalized telemetry/state estimates, not claims of validated production thresholds.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np


def _clip01(x: float) -> float:
    return float(np.clip(x, 0.0, 1.0))


def spectral_resilience(rho: float) -> float:
    return 1.0 - float(rho)


def capacity_margin(sigma_star: float) -> float:
    return 1.0 - float(sigma_star)


def capacity_adjusted_sri(rho: float, sigma_star: float) -> float:
    return spectral_resilience(rho) * capacity_margin(sigma_star)


def customer_impact_amplification(Hc: np.ndarray, J: np.ndarray, t: float = 1.0) -> float:
    """CIA(t) = || Hc exp(J t) ||_2, using an eigen-decomposition approximation."""
    Hc = np.asarray(Hc, dtype=float)
    J = np.asarray(J, dtype=float)
    vals, vecs = np.linalg.eig(J)
    inv = np.linalg.pinv(vecs)
    propagator = np.real_if_close(vecs @ np.diag(np.exp(vals * t)) @ inv).real
    return float(np.linalg.norm(Hc @ propagator, ord=2))


def reliability_adjusted_sri(rho: float, sigma_star: float, cia: float, alpha: float = 1.0) -> float:
    return capacity_adjusted_sri(rho, sigma_star) * math.exp(-alpha * max(0.0, cia))


def customer_experience_quality(
    availability: float,
    latency_s: float,
    error_rate: float,
    functional_quality: float = 1.0,
    recovery_quality: float = 1.0,
    latency_ref_s: float = 1.0,
    error_ref: float = 0.01,
    weights: tuple[float, float, float, float, float] = (0.2,) * 5,
) -> float:
    """Compute bounded CEQ from normalized customer-facing dimensions."""
    a = _clip01(availability)
    l = math.exp(-max(0.0, latency_s) / max(latency_ref_s, 1e-12))
    e = math.exp(-max(0.0, error_rate) / max(error_ref, 1e-12))
    f = _clip01(functional_quality)
    r = _clip01(recovery_quality)
    w = np.asarray(weights, dtype=float)
    if len(w) != 5 or w.sum() <= 0:
        raise ValueError("weights must contain five positive-total values")
    w = w / w.sum()
    return float(np.clip(np.dot(w, [a, l, e, f, r]), 0.0, 1.0))


def trust_stability(ceq: np.ndarray, volatility_ref: float = 1.0) -> float:
    variance = float(np.var(np.asarray(ceq, dtype=float)))
    return _clip01(1.0 - variance / max(volatility_ref, 1e-12))


def recovery_elasticity(ceq_baseline: float, ceq_min: float, recovery_time_s: float) -> float:
    if recovery_time_s <= 0:
        return 0.0
    return max(0.0, float(ceq_baseline) - float(ceq_min)) / recovery_time_s


def customer_reliability(ceq_series: np.ndarray, threshold: float = 0.8) -> float:
    values = np.asarray(ceq_series, dtype=float)
    if values.size == 0:
        return 0.0
    return float(np.mean(values >= threshold))


def customer_trust_index(
    rc: float, ts: float, recovery_elasticity_normalized: float, rsri: float,
    weights: tuple[float, float, float, float] = (0.25,) * 4,
) -> float:
    """Weighted geometric CTI; negative inputs are clipped to zero."""
    values = np.clip([rc, ts, recovery_elasticity_normalized, rsri], 0.0, 1.0)
    w = np.asarray(weights, dtype=float)
    if len(w) != 4 or np.any(w < 0) or w.sum() <= 0:
        raise ValueError("weights must contain four nonnegative values with positive sum")
    w = w / w.sum()
    return float(np.prod(np.power(values, w)))


@dataclass(frozen=True)
class CustomerReliabilitySnapshot:
    rho: float
    sigma_star: float
    cia: float
    rsri: float
    ceq: float
    customer_reliability: float
    trust_stability: float
    recovery_elasticity: float
    cti: float
