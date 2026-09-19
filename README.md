# fissionwatch

`fissionwatch` is an experimental Python toolkit for modeling customer-facing reliability from dependency-graph structure and telemetry.

The current package includes:

- customer reliability metrics from the paper notes in `PAPER_IMPLEMENTATION.md`
- Prometheus-compatible telemetry ingestion helpers
- a small CLI for quick metric calculations and version inspection

## Installation

Install from a checkout:

```bash
pip install .
```

Install with OpenTelemetry integration extras:

```bash
pip install ".[otel]"
```

For local development builds:

```bash
python -m build
```

## Python usage

```python
from fissionwatch import customer_experience_quality, reliability_adjusted_sri

ceq = customer_experience_quality(
    availability=0.995,
    latency_s=0.2,
    error_rate=0.002,
)
rsri = reliability_adjusted_sri(rho=0.2, sigma_star=0.5, cia=0.8)
```

Telemetry helpers can also build a dependency graph from a Prometheus-compatible API:

```python
from fissionwatch import graph_from_prometheus

graph = graph_from_prometheus("https://prometheus.example.com")
```

## CLI usage

Show the installed version:

```bash
fissionwatch version
```

Compute customer experience quality:

```bash
fissionwatch ceq --availability 0.995 --latency-s 0.2 --error-rate 0.002
```

Compute reliability-adjusted SRI:

```bash
fissionwatch rsri --rho 0.2 --sigma-star 0.5 --cia 0.8
```

## Release workflow

This repository includes a GitHub Actions workflow that:

- builds an sdist and wheel on pushes and tags
- validates the generated artifacts with `twine check`
- publishes to PyPI only for version tags matching `v*` using GitHub OIDC trusted publishing

Before tagging a release:

1. update `src/fissionwatch/_version.py`
2. commit the change
3. create and push a tag such as `v0.1.1`
4. ensure the repository is configured as a trusted publisher in PyPI

The workflow publishes only when the tagged version is intentionally released; it does not upload packages automatically from normal branch pushes.
