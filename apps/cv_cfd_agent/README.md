# CV → Flow Analysis Agent

A Streamlit proof of concept that converts a geometry image into an inspectable workflow:

1. **Vision agent** — decodes the image, thresholds foreground pixels, and extracts the largest contour.
2. **Geometry agent** — reports pixel area, perimeter, bounding box, and aspect ratio.
3. **Calculation agent** — computes external-flow screening quantities: Reynolds number, Mach screening value, dynamic pressure, and uncertainty ranges.
4. **Analysis agent** — renders a qualitative vector-field surrogate around the image mask.
5. **Report agent** — produces an evidence and validation-status summary.

## Run locally

```bash
cd apps/cv_cfd_agent
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Scope and safety boundary

This is **not a CFD solver**. The app supports bounded, low-speed external-flow screening only. It deliberately excludes combustion chemistry, internal chamber-pressure prediction, thrust calculation, nozzle optimization, thermal failure prediction, and structural safety sizing. These calculations could enable construction or optimization of a hazardous propulsion device and require qualified engineering workflows.

All image-derived geometry is approximate. For validated CFD, use a qualified solver with documented geometry, mesh, boundary conditions, material models, convergence criteria, uncertainty quantification, and experimental validation.
