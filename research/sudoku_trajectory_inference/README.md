# Sudoku-Inspired Probabilistic Trajectory Inference

This project adapts constraint-solving ideas from the paper *Applications Based on a Novel Sudoku Solver Algorithm and Grid Based Models* to inert, non-propelled test objects. It is intended for tracking, uncertainty estimation, measurement consistency, and algorithm validation—not propulsion or performance optimization.

## Features

- Synthetic 2D ballistic trajectory generation
- Gaussian measurement noise
- Candidate-state sampling using Monte Carlo particles
- Constraint filtering for physically plausible states
- Confidence intervals and RMSE evaluation
- Detection of inconsistent observations
- Visualization of true, measured, and estimated trajectories

## Run

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
python src/run_experiment.py
```

Outputs are written to `outputs/`.

## Sudoku-inspired mapping

| Sudoku concept | Trajectory inference analogue |
|---|---|
| Candidate values | Candidate position/velocity states |
| Fewest candidates | Most informative measurement/time step |
| Single assignment | State constrained to a narrow interval |
| Conflicting grid | Physically inconsistent measurements |
| Multiple solutions | Several trajectories consistent with observations |
| Dynamic random selection | Monte Carlo candidate generation |
