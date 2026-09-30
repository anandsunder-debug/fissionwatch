# Generic CFD / LBM Module

This directory contains the reusable numerical portion extracted from the uploaded CFD source archive.

## Included

- D2Q9 lattice-Boltzmann representation
- BGK collision operator
- equilibrium distribution
- macroscopic density/velocity recovery
- streaming
- half-way bounce-back boundary primitive
- deterministic field initialization

## Deliberately excluded

The original archive also contains application-specific flight dynamics, vehicle geometry, propulsion/jet parameters, combustion/scalar configuration, and launch scenarios. Those are not copied into this generic module.

## Intended integration

The module can be used as a numerical backend for:

1. synthetic flow-field experiments;
2. observability/resilience experiments where a CFD field is treated as a distributed state;
3. validation of SAI/SRI-style graph metrics over spatial grids;
4. future adapters for external CFD solvers.

The implementation is intentionally small and dependency-light so it can be tested independently.
