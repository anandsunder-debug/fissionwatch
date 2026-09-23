# SAI: Physarum-Inspired Knowledge Representation and Tensor Architecture

## Concept

Structural Adaptive Intelligence (SAI) is modeled as a **non-neural adaptive system** inspired by *Physarum polycephalum*. It does not require neurons, backpropagation, embeddings, or a learned neural network. Adaptation emerges from:

1. Explicit entities and typed relations.
2. Observed transitions between entities.
3. Conductance values stored in a third-order tensor.
4. Evaporation of stale pathways.
5. Reinforcement of frequently useful, low-cost transitions.

## Knowledge representation

- **Entity**: a named object such as a query, table, index, service, event, or workload state.
- **Relation**: a typed edge such as `reads`, `joins`, `blocks`, `depends_on`, or `transitions_to`.
- **Observation**: a timestamped event containing source, target, relation, weight, and cost.
- **State**: the current graph plus evidence and conductance tensors.

The core tensor is:

\[
C_{s,t,r} \ge 0
\]

where `s` is the source entity, `t` is the target entity, and `r` is the relation type.

## Adaptation rule

At each update, conductance undergoes evaporation and reinforcement:

\[
C_{s,t,r}^{(k+1)} = (1-\rho)C_{s,t,r}^{(k)} + \eta\frac{w}{c}
\]

for observed transitions, where `rho` is evaporation, `eta` is reinforcement, `w` is evidence weight, and `c` is transition cost.

This is a conceptual Physarum-inspired rule, not a biological simulation or a claim of cognitive behavior.

## Architecture

```text
Event stream / telemetry
          |
          v
Knowledge parser -> Entity registry -> Typed transition records
          |                         |
          +-------------> Transition tensor C[s,t,r]
                                      |
                        Evaporation + cost-aware reinforcement
                                      |
                         Structural state / path distribution
                                      |
                Recommendations, anomaly signals, workload adaptation
```

## Why this is non-neural

The system uses explicit symbolic identity, typed relations, deterministic tensor operations, and interpretable update rules. It can be implemented with NumPy or another tensor library without neurons, gradient descent, model training, or opaque latent representations.

## Database-indexing application

Entities can represent queries, tables, columns, indexes, and workload modes. Relations can represent `uses`, `filters_on`, `joins`, `competes_with`, and `transitions_to`. The model can then expose:

- Strong query-to-index pathways.
- Repeated bottleneck transitions.
- Stale or weakly supported paths.
- Workload-state changes from OLTP to OLAP or HYBRID.
- Candidate recommendations for human approval.

The current implementation remains recommendation-only. It must not issue automatic DDL against production databases without database-specific testing, approval, and rollback controls.
