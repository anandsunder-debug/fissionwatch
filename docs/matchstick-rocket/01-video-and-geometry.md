# Video and Geometry Reconstruction

## Video observations

The supplied frame-analysis poster identifies representative moments at approximately 0 ms, 8 ms, 20 ms, 40 ms, and 80 ms. These labels describe an observed sequence from initial position through ignition, visible thrust, motion blur, and flight.

A second visualization presents a calibrated geometry workflow using a ruler as a scale reference. The displayed overall length is approximately 38.1 mm in the illustrated reconstruction, while other views show differing diameter and component estimates. These differences must be retained as versioned assumptions rather than silently merged.

## Geometry representations

The supplied material includes several geometry variants:

- **Original / V1:** geometry reconstructed from the video.
- **Improved / V2:** a conceptual smoother-bend and tighter-seal variant.
- **Optimized / V3:** a further conceptual variant used in performance illustrations.

The posters show changes in body dimensions, bend geometry, nozzle dimensions, foil thickness, and estimated mass across versions. Because the underlying CAD source files and metrology records are not present here, these values should be stored as provisional metadata only.

## Recommended evidence fields

For each future measurement, record:

| Field | Description |
|---|---|
| Source frame | Frame number or timestamp |
| Reference object | Ruler or known dimension |
| Pixel measurement | Measured pixel length |
| Scale | Physical units per pixel |
| Estimated dimension | Converted physical dimension |
| Uncertainty | Calibration and segmentation uncertainty |
| Method | Manual, OpenCV, or other method |

## Reconstruction limitations

Perspective, lens distortion, occlusion, foil deformation, motion blur, and uncertain reference placement can materially affect dimensions. A CAD rendering is therefore a hypothesis about geometry until independently measured or supported by a source CAD file.
