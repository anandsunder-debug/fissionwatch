import numpy as np

def simulate_trajectory(times, initial_position=(0.0, 1.0), initial_velocity=(12.0, 10.0), gravity=9.81):
    """Simulate an inert object's 2D ballistic trajectory without propulsion."""
    times = np.asarray(times, dtype=float)
    x0, y0 = initial_position
    vx0, vy0 = initial_velocity
    x = x0 + vx0 * times
    y = y0 + vy0 * times - 0.5 * gravity * times**2
    vx = np.full_like(times, vx0)
    vy = vy0 - gravity * times
    return np.column_stack([x, y, vx, vy])

def add_measurement_noise(trajectory, position_sigma=0.15, seed=7):
    """Add independent Gaussian noise to measured x/y positions."""
    rng = np.random.default_rng(seed)
    measured = trajectory.copy()
    measured[:, :2] += rng.normal(0.0, position_sigma, size=(len(trajectory), 2))
    return measured
