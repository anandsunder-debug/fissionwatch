from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trajectory_model import simulate_trajectory, add_measurement_noise
from inference import generate_candidates, constrain_candidates, summarize_candidates

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

def main():
    times = np.linspace(0.0, 1.5, 31)
    truth = simulate_trajectory(times)
    measured = add_measurement_noise(truth)
    estimates, lower, upper, accepted_counts = [], [], [], []

    for i, measurement in enumerate(measured):
        candidates = generate_candidates(measurement, prior_position_sigma=0.5, prior_velocity_sigma=2.0, samples=4000, seed=100 + i)
        accepted = constrain_candidates(candidates, measured_position=measurement[:2], position_tolerance=0.35)
        summary = summarize_candidates(accepted)
        estimates.append(summary["mean"])
        lower.append(summary["lower_95"])
        upper.append(summary["upper_95"])
        accepted_counts.append(summary["count"])

    estimates, lower, upper = np.asarray(estimates), np.asarray(lower), np.asarray(upper)
    valid = np.isfinite(estimates[:, 0])
    rmse = np.sqrt(np.mean((estimates[valid, :2] - truth[valid, :2]) ** 2))
    print(f"Valid inference steps: {valid.sum()}/{len(times)}")
    print(f"Mean position RMSE: {rmse:.4f}")
    print(f"Mean accepted candidate count: {np.mean(accepted_counts):.1f}")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(truth[:, 0], truth[:, 1], label="True inertial trajectory")
    ax.scatter(measured[:, 0], measured[:, 1], s=18, label="Noisy observations")
    ax.plot(estimates[:, 0], estimates[:, 1], "--", label="Candidate mean")
    band = valid & np.isfinite(lower[:, 1]) & np.isfinite(upper[:, 1])
    ax.fill_between(estimates[band, 0], lower[band, 1], upper[band, 1], alpha=0.2, label="Candidate 95% vertical interval")
    ax.set_title("Sudoku-Inspired Constraint-Based Trajectory Inference")
    ax.set_xlabel("Horizontal position")
    ax.set_ylabel("Vertical position")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "trajectory_inference.png", dpi=160)
    plt.close(fig)

    np.savetxt(OUTPUT_DIR / "trajectory_results.csv", np.column_stack([times, truth, measured[:, :2], estimates]), delimiter=",", header="time,true_x,true_y,true_vx,true_vy,measured_x,measured_y,estimate_x,estimate_y,estimate_vx,estimate_vy", comments="")
    print(f"Saved outputs to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
