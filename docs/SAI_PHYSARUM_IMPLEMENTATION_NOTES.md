# Implementation Notes

- Use explicit symbolic entity IDs and typed relation IDs.
- Store adaptive conductance in a third-order tensor: source × target × relation.
- Apply evaporation on every observation cycle.
- Reinforce pathways according to evidence weight divided by transition cost.
- Expose normalized transition distributions for explainable recommendations.
- Keep database schema changes behind approval, benchmark, and rollback workflows.
- This design is not a neural network and does not perform gradient-based learning.
