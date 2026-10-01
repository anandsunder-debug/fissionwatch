# FissionWatch — Setup & Usage

This document is the practical setup guide for the current repository.

## 1. What is in the repository?

```text
fissionwatch/
├── apps/
│   └── cv_cfd_agent/       # Streamlit computer-vision research POC
├── docs/
│   ├── cfd/               # CFD/LBM documentation
│   └── matchstick-rocket/ # Research case-study documentation
├── research/
│   └── camphor_cfd/       # Research methodology
├── src/
│   ├── fissionwatch/       # Main FissionWatch package
│   ├── cfd/               # Generic D2Q9 LBM utilities
│   └── simulation/        # Geometry and trajectory utilities
├── tests/                 # Automated tests
├── examples/
├── experiments/
├── artifacts/
└── pyproject.toml
```

The Python project requires Python 3.10 or newer.

## 2. Prerequisites

Install:

- Python 3.10+
- Git
- pip

Check:

```bash
python --version
python -m pip --version
git --version
```

## 3. Clone

```bash
git clone https://github.com/anandsunder-debug/fissionwatch.git
cd fissionwatch
```

## 4. Create a virtual environment

### Linux / macOS / WSL

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Windows CMD

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

## 5. Install the project

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
```

The editable install is recommended for development because source changes are immediately available to the local environment. citeturn0search0turn0search9

For OpenTelemetry support:

```bash
python -m pip install -e ".[otel]"
```

## 6. Install pytest

```bash
python -m pip install pytest
```

Run the complete suite:

```bash
python -m pytest -v
```

Run CFD tests:

```bash
python -m pytest tests/test_lbm_d2q9.py -v
```

Run simulation tests:

```bash
python -m pytest tests/test_simulation.py -v
```

Running pytest from the repository root with a `src/` layout is consistent with the recommended Python project workflow. citeturn0search0turn0search10

## 7. Verify the CFD module

The generic LBM implementation is:

```text
src/cfd/lbm_d2q9.py
```

It provides:

- D2Q9 lattice
- equilibrium distribution
- macroscopic density/velocity recovery
- BGK collision
- streaming
- bounce-back boundary primitive
- field initialization

Verify the import:

```bash
python -c "from cfd.lbm_d2q9 import initialize; print(initialize(20,10).shape)"
```

Expected:

```text
(9, 10, 20)
```

The intended numerical flow is:

```text
initialize
  ↓
collision
  ↓
streaming
  ↓
boundary treatment
  ↓
repeat
```

The current implementation is a reusable numerical core, not a complete validated CFD application.

## 8. Verify post-processing

Use:

```text
src/cfd/postprocess.py
```

Example:

```python
import numpy as np
from cfd.postprocess import velocity_magnitude, field_summary

rho = np.ones((20, 40))
ux = np.zeros((20, 40))
uy = np.zeros((20, 40))

print(velocity_magnitude(ux, uy).shape)
print(field_summary(rho, ux, uy))
```

## 9. Use the geometry utilities

The generic geometry model is:

```text
src/simulation/geometry.py
```

Example:

```python
from simulation.geometry import profile_from_points

profile = profile_from_points([
    (0.00, 0.010),
    (0.05, 0.015),
    (0.10, 0.012),
])

print(profile.length)
print(profile.reference_area())
print(profile.radius_at(0.05))
```

The profile is represented as an ordered axis/radius dataset.

## 10. Use the trajectory model

The trajectory integrator is:

```text
src/simulation/flight_model.py
```

It supports:

- position
- velocity
- orientation
- angular velocity
- drag
- lift
- gravity
- externally supplied force/moment data
- RK4 integration

Example:

```python
import numpy as np
from simulation.flight_model import FlightState, FlightParameters, simulate

params = FlightParameters(
    mass=1.0,
    inertia=0.01,
    area=1e-3,
    cd=0.5,
    cl=0.0,
)

times = np.linspace(0.0, 2.0, 201)
initial = FlightState(vx=5.0, vy=10.0)

result = simulate(initial, params, times)

print(result[-1])
```

## 11. Run scenarios

Scenario orchestration is in:

```text
src/simulation/scenarios.py
```

A scenario contains:

```text
name
parameters
initial state
time vector
optional external force model
```

Example:

```python
import numpy as np
from simulation.flight_model import FlightState, FlightParameters
from simulation.scenarios import Scenario, run_scenario

scenario = Scenario(
    name="baseline",
    parameters=FlightParameters(mass=1.0, inertia=0.01, area=1e-3),
    initial=FlightState(vx=5.0, vy=10.0),
    times=np.linspace(0, 2, 201),
)

result = run_scenario(scenario)
print(result.shape)
```

## 12. Run the Streamlit application

The application is located at:

```text
apps/cv_cfd_agent/
```

Install its dependencies:

```bash
cd apps/cv_cfd_agent
python -m pip install -r requirements.txt
```

Run:

```bash
python -m streamlit run app.py
```

The application performs an image → geometry → qualitative flow-analysis → report workflow.

It is a research/visualization POC and should not be treated as a validated CFD solver.

## 13. Recommended development workflow

```bash
git pull --ff-only origin main

python -m pip install -e .
python -m pytest -v

git status
git diff
```

For larger changes:

```bash
git checkout -b feature/my-change
```

After testing:

```bash
git add .
git commit -m "Describe the change"
git push origin feature/my-change
```

## 14. CFD research workflow

Use this sequence for new numerical experiments:

```text
research question
      ↓
geometry representation
      ↓
computational domain
      ↓
numerical parameters
      ↓
initialization
      ↓
solver iterations
      ↓
boundary conditions
      ↓
convergence checks
      ↓
post-processing
      ↓
reference comparison
      ↓
sensitivity/refinement
      ↓
uncertainty + limitations
```

See:

```text
docs/cfd/README.md
docs/cfd/validation.md
research/camphor_cfd/methodology.md
```

A visualization alone is not validation. Record the computational assumptions, numerical parameters, convergence evidence, and independent comparison used to support a result.

## 15. External data integration

The trajectory model deliberately separates force/moment data from the integrator.

Conceptually:

```text
external data
    ↓
force/moment adapter
    ↓
simulation.flight_model
    ↓
trajectory
    ↓
post-processing
```

A future adapter can read CSV, JSON, HDF5, telemetry, or solver output and interpolate it onto the simulation time grid.

## 16. Current CLI note

`pyproject.toml` declares a `fissionwatch` console entry point, but the current `src/fissionwatch/` tree does not contain `cli.py`.

Therefore do not depend on the `fissionwatch` command yet. Use the Python modules, tests, examples, and applications directly.

This should be cleaned up later by either adding the intended CLI or removing the stale entry-point declaration.

## 17. Common problems

### ModuleNotFoundError

From the repository root:

```bash
python -m pip install -e .
```

Then:

```bash
python -c "import cfd; import simulation; print('imports OK')"
```

### pytest import problems

Run from the repository root:

```bash
python -m pytest -v
```

An editable install is recommended for a `src/` layout. citeturn0search0

### Streamlit not found

```bash
cd apps/cv_cfd_agent
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## 18. Clean reinstall

### Linux/macOS/WSL

```bash
deactivate 2>/dev/null || true
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
python -m pip install pytest
python -m pytest -v
```

### Windows PowerShell

```powershell
deactivate
Remove-Item -Recurse -Force .venv
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
python -m pip install pytest
python -m pytest -v
```

## 19. First successful run

The shortest verification path is:

```bash
git clone https://github.com/anandsunder-debug/fissionwatch.git
cd fissionwatch
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install pytest
python -m pytest -v
python -c "from cfd.lbm_d2q9 import initialize; print(initialize(20,10).shape)"
```

Expected final line:

```text
(9, 10, 20)
```

## 20. Architecture summary

```text
                         FissionWatch
                              │
             ┌────────────────┴────────────────┐
             │                                 │
      Reliability research                CFD research
             │                                 │
    graphs / telemetry                    D2Q9 core
    spectral analysis                         │
    resilience metrics                   post-processing
             │                                 │
             │                           geometry model
             │                                 │
             └──────────────────────┐    trajectory model
                                    │          │
                                    └──────────┘
                                         │
                                  validation/research
```

Keep numerical primitives, application logic, experiments, and documentation separated. This makes the repository easier to test, extend, and reproduce.

## References

- Repository: https://github.com/anandsunder-debug/fissionwatch
- CFD overview: `docs/cfd/README.md`
- Geometry: `docs/cfd/geometry.md`
- Validation: `docs/cfd/validation.md`
- Research methodology: `research/camphor_cfd/methodology.md`
- CV application: `apps/cv_cfd_agent/README.md`
