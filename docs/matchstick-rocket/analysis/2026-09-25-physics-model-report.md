# Video-Derived Physics Model

## Acquisition
- Video: VID20260925002844.mp4
- Resolution: 720 × 1280 px
- FPS: 60.009
- Frames: 926
- Duration: 15.431 s
- Geometry candidates: 24

## Geometry
Edge/contrast segmentation produced image-space bounding-box candidates. No physical mm/px calibration marker is present, so the model does not claim independently measured physical dimensions.

## Physics model
The simulation uses:
1. external flow around the video-derived body;
2. continuity and momentum equations;
3. a generic normalized heat-release/source term for the observed luminous plume;
4. passive scalar transport for plume/thermal signature;
5. gravity and aerodynamic drag as trajectory-level terms.

The source is deliberately not mapped to a specific pyrotechnic formulation, burn-rate law, chamber pressure, nozzle sizing, or propellant recipe.

## Equations
Continuity: ∂ρ/∂t + ∇·(ρu) = 0

Momentum: ∂(ρu)/∂t + ∇·(ρu⊗u) = −∇p + ∇·τ + ρg

Energy: ∂(ρE)/∂t + ∇·[(ρE+p)u] = ∇·(k∇T) + Q̇_generic

Passive plume scalar: ∂C/∂t + u·∇C = D∇²C + S_generic

Trajectory: m dV/dt = F_aero + F_gravity + F_generic

These equations define the computational framework; the video constrains geometry, timing and plume appearance but not chemical composition, temperature, pressure, mass flow, or thrust.