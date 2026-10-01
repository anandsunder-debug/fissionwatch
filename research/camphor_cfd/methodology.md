# Camphor test-article CFD: repository methodology

This directory records the methodology used to organize the uploaded research source.

Computational pipeline:

geometry -> flow solver -> field post-processing -> external force/moment data -> trajectory integration

The reusable implementation in src/cfd and src/simulation focuses on numerical methods,
geometry representation, reproducibility, and validation.

## Source provenance

The integration was derived from the uploaded archive camphor_rocket_cfd_src.zip,
which contained lbm.c, lbm.js, flight.py, scenarios.py, build.py, assemble.py, and queue.sh.

## Scope boundary

The archive also contained code for combustion/plume generation and propulsion parameter
sweeps. Those components are not reproduced as executable repository code. The research
interface instead accepts externally generated or measured force/moment histories.
