# Safe External-Flow CFD Setup

## Scope
This package models only a **non-reactive external airflow surrogate**. It excludes:
- combustion or chemical-reaction modeling
- internal pressure/temperature prediction
- nozzle or chamber design
- thrust, impulse, or launch-performance estimation
- trajectory or propulsion optimization

## Geometry
- Length: 100.0 mm
- Diameter: 3.0 mm
- Radius: 1.5 mm
- Length-to-diameter ratio: 33.33
- Shape: straight cylindrical surrogate
- Axis: X
- Status: assumed dimensions; not video-verified

## Suggested computational domain
Use a rectangular or cylindrical far-field domain with generous clearance around the body.
For a qualitative external-flow study, maintain at least:
- 5 body diameters upstream
- 10 body diameters downstream
- 5 body diameters to each lateral boundary

These are starting geometry guidelines, not validated mesh-independence requirements.

## Boundary conditions
- Inlet: prescribed uniform velocity
- Outlet: fixed reference pressure / convective outflow
- Far field or side walls: slip/symmetry where appropriate
- Body: no-slip wall
- Fluid: incompressible, constant-property, non-reactive
- Turbulence: begin with laminar or a low-order RANS sensitivity study only if justified by the selected Reynolds-number range

## Mesh strategy
1. Use a coarse global mesh for debugging.
2. Add local refinement around the cylinder and wake.
3. Add boundary-layer inflation only if wall shear is being evaluated.
4. Perform at least three mesh levels and compare drag coefficient and wake statistics.
5. Do not treat a single mesh result as validated.

## Reported quantities
- pressure coefficient distribution
- wall shear stress
- drag coefficient
- wake velocity deficit
- qualitative separation and recirculation behavior
- mesh-sensitivity comparison

## Limitations
The straight cylinder is a surrogate and does not establish the actual geometry, material, internal structure, or operating conditions of the uploaded object. Experimental validation is required before drawing physical conclusions.
