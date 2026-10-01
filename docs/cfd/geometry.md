# Geometry and trajectory integration

The uploaded CFD project has been normalized into reusable research interfaces.

## Separation of concerns
1. src/cfd/ contains generic lattice-Boltzmann numerical utilities.
2. src/simulation/geometry.py represents an axisymmetric computational body.
3. src/simulation/flight_model.py integrates planar motion with aerodynamic drag/lift and an externally supplied force/moment callback.
4. src/simulation/scenarios.py runs reproducible parameterized cases.

The original uploaded files contain additional propulsion/combustion-specific logic.
That material is intentionally not copied into executable repository code.
External CFD or experimental force data can instead be supplied through the force
callback or a future data adapter.
