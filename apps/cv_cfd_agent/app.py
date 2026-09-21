"""CV-to-flow educational analysis app.

Includes image segmentation, scale calibration, external-flow estimates,
Reynolds/Mach screening, dynamic pressure, uncertainty propagation, and
qualitative field visualization. It deliberately excludes combustion,
internal pressure, thrust, nozzle optimization, and safety-critical sizing.
"""
from dataclasses import dataclass
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
        return {"area_px": 0.0, "perimeter_px": 0.0, "aspect_ratio": None, "bbox": None}
    x, y, w, h = obs.bbox
    area = float(cv2.contourArea(obs.contour))
    perimeter = float(cv2.arcLength(obs.contour, True))
    return {
        "area_px": area,
        "perimeter_px": perimeter,
        "aspect_ratio": float(w / max(h, 1)),
        "bbox": {"x": x, "y": y, "width": w, "height": h},
    }


def external_flow_calculations(geometry: dict, length_m: float, velocity: float,
                               density: float, viscosity: float, uncertainty_pct: float) -> dict:
    """Bounded external-flow screening calculations, not a CFD solution."""
    reynolds = density * velocity * max(length_m, 0.0) / max(viscosity, 1e-12)
    sound_speed = 343.0
    mach = velocity / sound_speed
    dynamic_pressure = 0.5 * density * velocity**2
    relative_uncertainty = max(0.0, uncertainty_pct) / 100.0
    return {
        "reference_length_m": length_m,
        "velocity_m_per_s": velocity,
        "density_kg_per_m3": density,
        "dynamic_viscosity_pa_s": viscosity,
        "reynolds_number": reynolds,
        "mach_number_at_343mps": mach,
        "dynamic_pressure_pa": dynamic_pressure,
        "screening_uncertainty_fraction": relative_uncertainty,
        "reynolds_range": [reynolds * (1 - relative_uncertainty), reynolds * (1 + relative_uncertainty)],
        "interpretation": "Low-speed external-flow screening; not a validated solver result.",
    }


def surrogate_flow_agent(obs: Observation, grid_size: int = 180):
    h, w = obs.mask.shape[:2]
    scale = min(grid_size / max(w, 1), grid_size / max(h, 1))
    small = cv2.resize(obs.mask, (max(10, int(w * scale)), max(10, int(h * scale))))
    small = (small > 0).astype(np.uint8)
    sh, sw = small.shape
    yy, xx = np.mgrid[0:sh, 0:sw]
    cx, cy = sw * 0.25, sh * 0.5
    dx, dy = xx - cx, yy - cy
    r2 = dx * dx + dy * dy + 8.0
    u = 1.0 - 0.25 * dx / r2
    v = -0.25 * dy / r2
    u[small > 0] = np.nan
    v[small > 0] = np.nan
    speed = np.sqrt(u * u + v * v)
    return u, v, speed


def report_agent(geometry: dict, calculations: dict) -> str:
    return ("## Agent report\n"
            f"- Segmented area: `{geometry['area_px']:.1f} px²`\n"
            f"- Perimeter: `{geometry['perimeter_px']:.1f} px`\n"
            f"- Reynolds number: `{calculations['reynolds_number']:.3g}`\n"
            f"- Mach screening value: `{calculations['mach_number_at_343mps']:.3g}`\n"
            f"- Dynamic pressure: `{calculations['dynamic_pressure_pa']:.3f} Pa`\n"
            "- Status: external-flow screening and qualitative visualization only.\n")


st.set_page_config(page_title="CV → Flow Analysis Agent", layout="wide")
st.title("CV → Flow Analysis Agent")
st.caption("Vision → geometry → bounded calculations → qualitative visualization → report")
st.warning("Safety boundary: this app excludes combustion, internal pressure, thrust, nozzle optimization, and safety-critical sizing.")

with st.sidebar:
    st.header("External-flow inputs")
    length_m = st.number_input("Reference length (m)", min_value=1e-6, value=0.05, format="%.6f")
    velocity = st.number_input("Freestream velocity (m/s)", min_value=0.0, value=10.0)
    density = st.number_input("Fluid density (kg/m³)", min_value=1e-6, value=1.225)
    viscosity = st.number_input("Dynamic viscosity (Pa·s)", min_value=1e-8, value=1.81e-5, format="%.8f")
    uncertainty = st.slider("Input uncertainty (%)", 0.0, 50.0, 10.0)

uploaded = st.file_uploader("Upload a poster, CAD screenshot, or geometry image", type=["png", "jpg", "jpeg"])
if uploaded:
    obs = vision_agent(uploaded.getvalue())
    geometry = geometry_agent(obs)
    calculations = external_flow_calculations(geometry, length_m, velocity, density, viscosity, uncertainty)
    u, v, speed = surrogate_flow_agent(obs)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Vision agent")
        st.image(cv2.cvtColor(obs.image, cv2.COLOR_BGR2RGB), use_container_width=True)
        st.image(obs.mask, caption="Thresholded silhouette", use_container_width=True)
    with c2:
        st.subheader("Analysis agent")
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.imshow(speed, origin="upper")
        step = max(1, speed.shape[0] // 24)
        ax.quiver(u[::step, ::step], v[::step, ::step])
        ax.set_title("Qualitative vector field (not CFD)")
        ax.set_axis_off()
        st.pyplot(fig, clear_figure=True)

    st.subheader("Geometry output")
    st.json(geometry)
    st.subheader("Bounded engineering calculations")
    st.json(calculations)
    st.markdown(report_agent(geometry, calculations))
else:
    st.info("Upload an image to run the pipeline.")
