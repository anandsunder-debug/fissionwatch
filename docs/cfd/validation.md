# CFD validation workflow

Validation should proceed from simple to coupled cases:

- Verify uniform-field preservation and collision behavior with unit tests.
- Compare generic flow-field summaries against analytical/reference cases.
- Perform grid and time-step refinement before interpreting coefficients.
- Keep geometry, solver settings, boundary conditions, and sampled outputs versioned.
- Compare trajectory integrations against independently measured kinematics when available.

The repository intentionally separates force generation from flight integration;
this prevents a trajectory result from being mistaken for validation of a particular
propulsion or combustion model.
