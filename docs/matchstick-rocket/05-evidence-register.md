# Evidence Register

This register distinguishes the material's evidentiary status.

| Artifact or claim | Classification | Required support |
|---|---|---|
| Video frame sequence | Observation | Original video, metadata, frame extraction log |
| Approximate dimensions | Derived estimate | Scale reference, calibration method, uncertainty |
| CAD-style renderings | Reconstruction hypothesis | Source CAD or documented geometry assumptions |
| Exploded views | Conceptual decomposition | Component definitions and dimensional basis |
| Temperature and pressure maps | Illustrative/model-generated | Solver case, thermophysical data, mesh, convergence |
| Velocity and streamline maps | Illustrative/model-generated | Flow model, boundary conditions, mesh, solver outputs |
| Structural stress map | Illustrative/model-generated | Material model, loads, constraints, mesh, convergence |
| Motion-tracking curve | Derived estimate | Tracked coordinates, calibration, frame timing |
| Thrust and impulse values | Unverified estimate unless raw data exists | Force-time data, calibration, uncertainty, repeat trials |
| Range and maximum-height values | Model or observation dependent | Complete trajectory data and coordinate definitions |

## Version control principle

When a later analysis changes a dimension, model assumption, or result, retain the previous value in a dated revision record. Do not overwrite measured, estimated, and simulated values in one undifferentiated table.

## Reproducibility status

At the time of this documentation commit, the supplied visual material supports a coherent case-study narrative but does not include all raw video, CAD, solver, mesh, and experimental datasets needed for full reproduction.
