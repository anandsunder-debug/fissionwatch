# Video-Constrained External Reconstruction Artifacts

This directory contains safe, non-reactive external-envelope artifacts derived from the uploaded video workflow.

## Scope and limitations
- Dimensions used: 100 mm length and 3 mm diameter, supplied as assumptions.
- The video does not provide enough calibration or multiple views for a validated 3-D reconstruction.
- The model excludes internal chambers, combustion, nozzle design, pressure prediction, thrust estimation, trajectory optimization, and fabrication guidance.
- CFD guidance is limited to qualitative external airflow around an inert surrogate.

## Contents
- `external_flow_cfd_setup.md` — external-flow CFD setup notes.
- `surrogate_profile.csv` — assumed cylindrical profile.
- `video_constrained_solid_model.scad` — editable OpenSCAD solid.
- `model_metadata.json` — geometry assumptions and scope.
- `safe_external_flow_model_100mm_x_3mm.zip` — packaged external-flow model artifacts.

The package is intended for visualization, geometry exchange, and safe non-reactive external-flow studies only.
