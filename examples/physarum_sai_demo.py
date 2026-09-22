from sai_core import Entity, Transition, StructuralAdaptiveTensor

entities = [
    Entity("q_customer_date", "query"),
    Entity("idx_customer_date", "index"),
    Entity("customer_table", "table"),
    Entity("oltp", "workload"),
]
relations = ["uses", "reads", "runs_in", "transitions_to"]
model = StructuralAdaptiveTensor(entities, relations)

# Seed explicit knowledge and observed transitions.
model.ingest([
    Transition(0, 1, 0, weight=4.0, cost=1.0),
    Transition(0, 2, 1, weight=2.0, cost=2.0),
    Transition(0, 3, 2, weight=1.0, cost=1.0),
])
model.adapt([
    Transition(0, 1, 0, weight=3.0, cost=1.0),
    Transition(0, 2, 1, weight=1.0, cost=3.0),
])

print("Transition distribution from query via 'uses':")
print(model.transition_distribution(source=0, relation=0))
print("Strongest adaptive pathways:")
for row in model.strongest_transitions():
    print(row)
