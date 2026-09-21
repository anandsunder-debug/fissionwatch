# Physics and Modeling Framework

## Model layers

The prior visualizations combine several physical domains. They should be treated as separate model layers with explicit interfaces:

1. **Observation layer:** video frames, timestamps, scale references, and tracked position.
2. **Geometry layer:** component boundaries, dimensions, and CAD-style representations.
3. **Thermal layer:** qualitative heat distribution and temperature-field visualization.
4. **Fluid layer:** internal and external flow concepts, pressure, velocity, and streamlines.
5. **Structural layer:** foil/jacket deformation and stress visualization.
6. **Motion layer:** position, velocity, acceleration, and trajectory comparison.

## Governing concepts shown in the source material

The posters reference general relationships such as:

- Ideal-gas behavior: `pV = nRT`
- Momentum-based thrust representation: `F = m_dot v_e + (p_e - p_a) A_e`
- Energy release and thermal transport
- Compressible-flow and possible choking concepts
- Projectile or force-driven motion models

These equations are useful as conceptual labels, but they are not sufficient to validate a combustion system. A defensible model would require experimentally supported thermochemical properties, transient mass generation, heat transfer, material response, pressure losses, and boundary conditions.

## Modeling discipline

Each equation or field should be accompanied by:

- Assumptions and applicability range
- Initial and boundary conditions
- Parameter source and uncertainty
- Numerical method and discretization
- Verification checks
- Validation data, if available

The present repository records the conceptual framework without treating the displayed performance estimates as validated engineering specifications.
