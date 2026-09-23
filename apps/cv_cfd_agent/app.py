"""Educational CV-to-flow-analysis app.

This app extracts approximate 2-D geometry from an uploaded image and renders a
non-validated, incompressible potential-flow surrogate for visual inspection.
It is not a combustion, pressure-vessel, nozzle, or propulsion design tool.
"""
from dataclasses import dataclass
from pathlib import Path
import cv2
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


@dataclass
class Observation:
    image: np.ndarray
    mask: np.ndarray
    contour: np.ndarray | None
    bbox: tuple[int, int, int, int] | None


def vision_agent(image_bytes: bytes) -> Observation:
    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Could not decode image")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, mask = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = max(contours, key=cv2.contourArea) if contours else None
    bbox = cv2.boundingRect(contour) if contour is not None else None
    return Observation(image, mask, contour, bbox)


def geometry_agent(obs: Observation) -> dict:
    if obs.contour is None or obs.bbox is None:
        return {"area_px": 0.0, "aspect_ratio": None, "bbox": None}
    x, y, w, h = obs.bbox
    return {
        "area_px": float(cv2.contourArea(obs.contour)),
        "aspect_ratio": float(w / max(h, 1)),
        "bbox": {"x": x, "y": y, "width": w, "height": h},
    }


def surrogate_flow_agent(obs: Observation, grid_size: int = 180):
    """Create a qualitative flow-like field around the detected silhouette.

    This is a visualization surrogate, not a CFD solver and must not be used
    for engineering decisions or operating-condition selection.
    """
    h, w = obs.mask.shape[:2]
    scale = min(grid_size / max(w, 1), grid_size / max(h, 1))
    small = cv2.resize(obs.mask, (max(10, int(w * scale)), max(10, int(h * scale))))
    small = (small > 0).astype(np.uint8)
    sh, sw = small.shape
    yy, xx = np.mgrid[0:sh, 0:sw]
    cx = sw * 0.25
    cy = sh * 0.5
    dx = xx - cx
    dy = yy - cy
    r2 = dx * dx + dy * dy + 8.0
    u = 1.0 - 0.25 * dx / r2
    v = -0.25 * dy / r2
    u[small > 0] = np.nan
    v[small > 0] = np.nan
    speed = np.sqrt(u * u + v * v)
    return u, v, speed, small


def report_agent(geometry: dict) -> str:
    return (
        "## Agent report\n"
        f"- Segmented area: `{geometry['area_px']:.1f} px²`\n"
        f"- Bounding-box aspect ratio: `{geometry['aspect_ratio']}`\n"
        "- Flow result: qualitative surrogate only\n"
        "- Validation status: no mesh, boundary conditions, solver convergence, "
        "material model, or experimental calibration supplied\n"
    )


st.set_page_config(page_title="CV → Flow Analysis Agent", layout="wide")
st.title("CV → Flow Analysis Agent")
st.caption("Educational image-to-geometry workflow with a qualitative flow surrogate")
st.warning("Not validated CFD. Do not use for combustion, pressure, propulsion, or safety-critical design.")

uploaded = st.file_uploader("Upload a poster, CAD screenshot, or geometry image", type=["png", "jpg", "jpeg"])
if uploaded:
    obs = vision_agent(uploaded.getvalue())
    geometry = geometry_agent(obs)
    u, v, speed, small = surrogate_flow_agent(obs)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Vision agent: segmentation")
        st.image(cv2.cvtColor(obs.image, cv2.COLOR_BGR2RGB), use_container_width=True)
        st.image(obs.mask, caption="Thresholded silhouette", use_container_width=True)
    with c2:
        st.subheader("Analysis agent: qualitative field")
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.imshow(speed, origin="upper")
        step = max(1, speed.shape[0] // 24)
        ax.quiver(u[::step, ::step], v[::step, ::step])
        ax.set_title("Surrogate vector field (not CFD)")
        ax.set_axis_off()
        st.pyplot(fig, clear_figure=True)

    st.subheader("Geometry agent output")
    st.json(geometry)
    st.markdown(report_agent(geometry))
else:
    st.info("Upload an image to run the vision → geometry → analysis → report pipeline.")
