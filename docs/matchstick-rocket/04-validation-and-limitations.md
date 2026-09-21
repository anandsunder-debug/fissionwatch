# Validation and Limitations

## Comparison categories

The project contains comparisons between video tracking, analytical trajectory concepts, and simulated curves. These comparisons should be reported in three categories:

### 1. Directly observed

Examples include visible ignition timing, apparent movement, motion blur, and frame-to-frame position. These require the original video and a documented frame extraction method for reproducibility.

### 2. Derived from observation

Examples include scale-calibrated dimensions, displacement, approximate velocity, and trajectory coordinates. These require camera calibration, reference-scale placement, frame rate, tracking uncertainty, and coordinate-system definition.

### 3. Model-generated

Examples include pressure, temperature, thrust, exit velocity, structural stress, and predicted range. These require complete model inputs and validation data before they can be treated as quantitative results.

## Validation checklist

- [ ] Preserve original video and metadata.
- [ ] Record camera frame rate and shutter settings.
- [ ] Calibrate spatial scale and camera perspective.
- [ ] Publish tracked coordinates and uncertainty.
- [ ] Separate fitted parameters from independently measured parameters.
- [ ] Record solver, mesh, timestep, and convergence information.
- [ ] Compare predictions against independent observations.
- [ ] Report error bars and failed or excluded trials.
- [ ] Avoid presenting illustrative values as measured performance.

## Current limitations

The supplied posters do not, by themselves, provide sufficient raw evidence to verify all numerical values shown in the CFD, structural, thrust, and trajectory panels. Consequently, this repository treats those panels as prior visual communication artifacts and documents a path toward reproducibility rather than claiming completed experimental validation.
