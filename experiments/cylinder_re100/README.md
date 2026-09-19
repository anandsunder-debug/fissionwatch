# CFD Validation Experiment: Re = 100 Cylinder

## Purpose
This experiment provides a reproducible, inert external-flow CFD benchmark for validating the numerical workflow used by FissionWatch-related engineering simulations. It is deliberately separated from combustion, internal-pressure, ignition, nozzle, and thrust modeling.

## Physical problem
- Geometry: two-dimensional circular cylinder represented by a thin STL surface
- Flow: transient, incompressible, laminar, Newtonian
- Reynolds number: Re = 100
- Diameter: D = 1 m
- Free-stream velocity: U = 1 m/s
- Kinematic viscosity: nu = 0.01 m^2/s
- Domain: approximately -15D to +25D in x and +/-15D in y

## Validation targets
The case uses established benchmark ranges as acceptance targets, not as precomputed results:

| Quantity | Target |
|---|---:|
| Mean drag coefficient | approximately 1.33–1.37 |
| Strouhal number | approximately 0.160–0.166 |

A run must not be called validated until residual behavior, mesh convergence, time-step sensitivity, and force-signal quality have been documented.

## Execution
1. Install and source a compatible OpenFOAM release.
2. Extract the case package supplied with this experiment.
3. Check the dictionaries against the installed release because syntax and library names can differ by version.
4. Run `chmod +x Allrun && ./Allrun`.
5. Inspect the generated fields and force history in ParaView and with post-processing tools.

## Validation gates
- `checkMesh` reports acceptable quality.
- Residuals and continuity remain controlled.
- At least three mesh resolutions are compared.
- At least two time steps are compared.
- Mean drag variation between the two finest meshes is below 2%.
- The dominant lift frequency is within roughly 5% of the benchmark range.
- The lift signal exhibits sustained periodic vortex shedding.
- The report records solver version, mesh size, time step, runtime, convergence settings, and uncertainty.

## Use cases
1. **CFD workflow verification:** test meshing, transient solving, force extraction, and post-processing.
2. **Numerical regression testing:** compare solver changes, discretization schemes, and convergence settings.
3. **Telemetry-to-physics research:** transform force, residual, oscillation, and frequency signals into stability indicators.
4. **Digital-twin prototyping:** use a controlled benchmark before ingesting telemetry from complex enterprise or physical systems.
5. **Visualization:** generate velocity, pressure, vorticity, and wake animations in ParaView.

## Limitations
- The case is a starting template and has not been executed in this environment.
- No CFD result, drag value, frequency, or validation certificate is claimed here.
- The cylinder case is not a model of a matchstick, improvised rocket, combustion chamber, or propulsion device.
- The STL and OpenFOAM dictionaries should be reviewed for the exact OpenFOAM version used.

## Relationship to FissionWatch
FissionWatch can use the experiment conceptually as a controlled signal source: solver residuals, force coefficients, oscillation amplitude, and frequency can be represented as time-series telemetry and evaluated for stability, perturbation, and cascade-like behavior. This is an analytical integration pattern, not a claim that CFD output alone proves software-fission behavior.
