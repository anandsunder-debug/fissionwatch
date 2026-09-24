# Computer-Vision / Combustion-Modeling Readiness Report

## Video
- Resolution: 720 × 1280 px
- Frame rate: 60.009 FPS
- Frames: 926
- Duration: 15.431 s

## Why this video is useful
The object remains visible for much of the recording and there are repeated high-intensity warm/orange plume events. This makes it useful for frame-by-frame object tracking, plume segmentation, centroid/apparent-area tracking, event timing, optical-flow estimation, and qualitative CFD-field reconstruction.

## Current CV extraction
The accompanying CSV contains frame number, timestamp, warm/plume pixel count, and plume centroid in pixels. A pixel-to-mm calibration is still required before reporting physical dimensions.

## Modeling abstraction
For safe research use, the video constrains the shape and timing of a generic heat-release source field rather than identifying a specific pyrotechnic formulation.

- Continuity: d(rho)/dt + div(rho*u) = 0
- Momentum: d(rho*u)/dt + div(rho*u*u) = -grad(p) + div(tau) + rho*g
- Energy: d(rho*h)/dt + div(rho*u*h) = div(k*grad(T)) + Q_dot_generic
- Generic scalar transport for a normalized plume/thermal variable.

The video does not independently determine temperature, pressure, composition, burn rate, or thrust.

## FBD
The FBD is conceptual. Force magnitudes should come from independently measured mass, acceleration/trajectory, and aerodynamic characterization.

## Geometry status
Earlier 100 mm × 3 mm dimensions are study priors only; this video does not establish those dimensions in millimetres.