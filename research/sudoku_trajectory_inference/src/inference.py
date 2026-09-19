import numpy as np

def generate_candidates(measurement, prior_position_sigma=0.5, prior_velocity_sigma=2.0, samples=3000, seed=11):
    """Generate candidate states around a position measurement."""
    rng = np.random.default_rng(seed)
    position = measurement[:2] + rng.normal(0.0, prior_position_sigma, size=(samples, 2))
    velocity = rng.normal(0.0, prior_velocity_sigma, size=(samples, 2))
    return np.column_stack([position, velocity])

def propagate_candidates(candidates, dt, gravity=9.81):
    """Propagate candidate states under inertial ballistic dynamics."""
    result = candidates.copy()
    result[:, 0] += result[:, 2] * dt
    result[:, 1] += result[:, 3] * dt - 0.5 * gravity * dt**2
    result[:, 3] -= gravity * dt
    return result

def constrain_candidates(candidates, measured_position, position_tolerance=0.35, require_nonnegative_height=True):
    """Filter candidates using measurement and basic physical constraints."""
    distance = np.linalg.norm(candidates[:, :2] - measured_position[None, :], axis=1)
    mask = distance <= position_tolerance
    if require_nonnegative_height:
        mask &= candidates[:, 1] >= 0.0
    return candidates[mask]

def summarize_candidates(candidates):
    """Return mean and 95% interval for candidate state components."""
    if len(candidates) == 0:
        return {"count": 0, "mean": np.full(4, np.nan), "lower_95": np.full(4, np.nan), "upper_95": np.full(4, np.nan)}
    return {"count": len(candidates), "mean": np.mean(candidates, axis=0), "lower_95": np.percentile(candidates, 2.5, axis=0), "upper_95": np.percentile(candidates, 97.5, axis=0)}

def position_rmse(estimate, truth):
    estimate = np.asarray(estimate)
    truth = np.asarray(truth)
    return float(np.sqrt(np.mean((estimate[:, :2] - truth[:, :2]) ** 2)))
