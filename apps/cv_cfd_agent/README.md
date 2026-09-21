# CV → Flow Analysis Agent

A lightweight Streamlit proof of concept that converts a geometry image into an inspectable analysis workflow:

1. **Vision agent** — decodes the image, thresholds foreground pixels, and extracts the largest contour.
2. **Geometry agent** — reports pixel area, bounding box, and aspect ratio.
3. **Analysis agent** — renders a qualitative vector-field surrogate around the image mask.
4. **Report agent** — produces an evidence and validation-status summary.

## Run locally

```bash
cd apps/cv_cfd_agent
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Scope and limitations

This is **not a CFD solver**. It does not calculate combustion, chamber pressure, thrust, nozzle performance, thermal loads, or structural safety. The plotted field is a qualitative visualization surrogate and should not be used to construct, optimize, or operate a propulsion device. For validated CFD, use a qualified solver with documented geometry, mesh, boundary conditions, material models, convergence criteria, and experimental validation.
