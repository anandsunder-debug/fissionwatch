# CANCE — Generic Causal Graph & Counterfactual Narrative Engine

CANCE is a Streamlit prototype for representing any story, scenario, operational incident, or system as a directed causal graph, applying a counterfactual intervention to a node, tracing reachable downstream nodes, and generating alternative narrative hypotheses.

## Capabilities

- Model plot events, actors, decisions, system states, and outcomes as nodes.
- Specify directed causal dependencies with a mechanism and qualitative edge strength.
- Highlight the intervention node and reachable downstream nodes in a graph visualization.
- Generate 3–10 alternative outcome narratives through different causal lenses.
- Trace each branch through baseline, intervention, graph dependencies, downstream reachability, decision response, and outcome synthesis.
- Add character, system, chronology, and world constraints.
- Export graph, assumptions, causal chains, and branches to Markdown or JSON.
- Validate unknown edge endpoints and detect directed cycles.

## Quick start

Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit, usually http://localhost:8501.

## Define a graph

In the sidebar, enter nodes one per line:

```text
start | Initial situation | state
decision | Protagonist makes a choice | decision
consequence | Immediate consequence | event
outcome | Downstream outcome | outcome
```

Node IDs must contain only letters, numbers, and underscores. Then define edges:

```text
start -> decision | creates decision context | medium
decision -> consequence | action causes consequence | medium
consequence -> outcome | downstream dependency | unknown
```

Edge strengths are qualitative labels (low, medium, high, unknown), not probabilities. Choose a target node ID, describe the intervention, and generate branches.

## How it works

1. **Baseline graph:** nodes and directed edges represent the causal model supplied by the user.
2. **Intervention:** change a specific node or the conditions associated with it.
3. **Propagation:** breadth-first reachability identifies downstream nodes connected by encoded edges.
4. **Counterfactual lenses:** the engine develops hypotheses around information, options, trust, timing, feedback, strategic response, path dependence, agency, contingency, and resources.
5. **Traceability:** reports retain graph edges, their mechanisms, the intervention, assumptions, and each generated causal step.

If the node editor is emptied, the optional fallback can split the plot into sentences and connect them in sentence order. This is only a provisional scaffold, not semantic causal extraction.

## Important limitations

- This is an **auditable prototype**, not a validated causal inference system or autonomous causal-discovery model.
- Graph reachability means a downstream node is connected in the encoded graph; it does not prove that an intervention will cause that event.
- Narrative branches are qualitative hypotheses, not canonical facts or predictions. No calibrated probabilities are computed.
- The default graph is a starter template. Replace its nodes and edges for each scenario before interpreting results.
- The sentence-order fallback infers only textual order; it must not be treated as a causal graph without review.
- This version does not yet use an LLM to extract actors, events, temporal states, causal relations, or evidence from a plot.
- The graph validator expects a directed acyclic graph (DAG). Represent feedback as a later time-indexed state instead of a cycle.

## Next research-grade steps

- Add LLM-assisted entity/event extraction with source-span provenance.
- Separate observed facts, user assumptions, inferred links, and generated hypotheses.
- Add temporal nodes, intervention values, and explicit structural equations or qualitative state-transition rules.
- Score counterfactual branches against minimal-change consistency, character/system invariants, edge support, and contradictions.
- Add tests for graph traversal, cycle detection, edge validation, and report reproducibility.

## Repository layout

```
cance/
  app.py
  requirements.txt
  README.md
  tests/
    test_cance.py
```

## License

No license is declared by this prototype. Add a license before redistributing if needed.
