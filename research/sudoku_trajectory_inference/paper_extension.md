# Suggested Manuscript Extension

## Constraint-Based Probabilistic State Inference for Inertial Trajectory Reconstruction

The Sudoku-inspired method can be interpreted as a constraint satisfaction process over a continuous state space. At each observation time, a set of candidate states is generated, then reduced by measurement compatibility and basic physical constraints.

Let the state be:

\[
\mathbf{x}_k = [x_k, y_k, v_{x,k}, v_{y,k}]^T.
\]

The candidate set is:

\[
\mathcal{C}_k = \left\{\mathbf{x}^{(i)}_k : \|\mathbf{p}^{(i)}_k-\mathbf{z}_k\|_2 \leq \epsilon,\quad y^{(i)}_k \geq 0\right\}.
\]

Here, \(\mathbf{z}_k\) is the measured position and \(\epsilon\) is the measurement compatibility tolerance.

The method preserves multiple feasible hypotheses rather than forcing an early single solution. A narrow candidate distribution indicates stronger state determination, whereas a broad distribution indicates uncertainty or insufficient measurements.

## Validation metrics

- Position RMSE
- Candidate-set survival rate
- 95% interval coverage
- Mean candidate-set size
- Outlier/inconsistency detection rate
- Sensitivity to measurement noise

## Limitation

This framework supports inertial tracking and uncertainty analysis. It does not estimate, optimize, or model combustion, thrust, nozzle geometry, or propulsion performance.
