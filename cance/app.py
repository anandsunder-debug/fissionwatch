from __future__ import annotations
import json, re
from collections import deque
from datetime import datetime, timezone
from typing import Any
import streamlit as st

APP_VERSION = "0.3.0"
LENSES = [
("Information / belief revision", "The changed condition alters what an actor knows or believes."),
("Options / resources", "The intervention changes which actions are feasible."),
("Trust / coordination", "The intervention changes cooperation, conflict, or access to help."),
("Timing / commitment", "The intervention changes when a decision becomes binding."),
("Feedback / adaptation", "Other actors respond and can amplify or dampen the initial effect."),
("Strategic response", "An opposing actor adapts to protect their own objective."),
("Path dependence", "A small early change compounds through later dependencies."),
("Agency / value conflict", "The protagonist chooses differently because priorities are reconsidered."),
("Contingency / risk", "An uncertain external event changes the trajectory."),
("Resource constraint", "Time, money, evidence, authority, or capacity constrains the response."),
]

def parse_nodes(raw: str) -> list[dict[str, str]]:
    nodes, seen = [], set()
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"): continue
        parts = [p.strip() for p in line.split("|", 2)]
        if len(parts) < 2: raise ValueError(f"Node line needs 'id | label | type': {line}")
        node_id, label = parts[0], parts[1]
        kind = parts[2] if len(parts) > 2 and parts[2] else "event"
        if not re.fullmatch(r"[A-Za-z0-9_]+", node_id): raise ValueError(f"Invalid node ID '{node_id}': use letters, numbers, underscores.")
        if node_id in seen: raise ValueError(f"Duplicate node ID: {node_id}")
        seen.add(node_id); nodes.append({"id": node_id, "label": label, "type": kind})
    return nodes

def infer_nodes_from_plot(plot: str) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    # Provisional fallback only: sentence order is not semantic causal discovery.
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", plot) if s.strip()][:20]
    nodes = [{"id": f"event_{i+1}", "label": s[:180], "type": "inferred_event"} for i, s in enumerate(sentences)]
    edges = [{"source": nodes[i]["id"], "target": nodes[i+1]["id"],
              "mechanism": "plot order (inferred, unverified)", "strength": "unknown",
              "basis": "Sentence-order heuristic"} for i in range(len(nodes)-1)]
    return nodes, edges

def parse_edges(raw: str, node_ids: set[str]) -> list[dict[str, Any]]:
    edges = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"): continue
        m = re.match(r"^([A-Za-z0-9_]+)\s*->\s*([A-Za-z0-9_]+)(?:\s*\|\s*([^|]+))?(?:\s*\|\s*(low|medium|high|unknown))?$", line, re.I)
        if not m: raise ValueError(f"Edge line needs 'source -> target | mechanism | strength': {line}")
        source, target, mechanism, strength = m.groups()
        if source not in node_ids or target not in node_ids: raise ValueError(f"Edge '{source} -> {target}' references an unknown node.")
        if source == target: raise ValueError(f"Self-loop not supported: {source} -> {target}")
        edges.append({"source": source, "target": target, "mechanism": (mechanism or "causal dependency").strip(),
                      "strength": (strength or "unknown").lower(), "basis": "User-specified causal edge"})
    return edges

def descendants(start: str, edges: list[dict[str, Any]]) -> list[str]:
    adj: dict[str, list[str]] = {}
    for e in edges: adj.setdefault(e["source"], []).append(e["target"])
    seen, queue, ordered = set(), deque(adj.get(start, [])), []
    while queue:
        cur = queue.popleft()
        if cur in seen or cur == start: continue
        seen.add(cur); ordered.append(cur); queue.extend(adj.get(cur, []))
    return ordered

def validate_graph(nodes: list[dict[str, str]], edges: list[dict[str, Any]]) -> list[str]:
    errors, ids = [], {n["id"] for n in nodes}
    if not nodes: errors.append("Add nodes or provide a plot to create a provisional sentence-chain graph.")
    indegree, adj = {i: 0 for i in ids}, {i: [] for i in ids}
    for e in edges:
        if e["source"] not in ids or e["target"] not in ids:
            errors.append(f"Unknown edge endpoint: {e['source']} -> {e['target']}"); continue
        adj[e["source"]].append(e["target"]); indegree[e["target"]] += 1
    q, visited = deque(i for i, d in indegree.items() if d == 0), 0
    while q:
        cur = q.popleft(); visited += 1
        for nxt in adj[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0: q.append(nxt)
    if visited != len(ids): errors.append("Graph contains a cycle. This prototype expects a DAG; represent feedback as a later time-indexed node.")
    return errors

def graph_dot(nodes: list[dict[str, str]], edges: list[dict[str, Any]], changed: str, affected: set[str]) -> str:
    lines = ["digraph CANCE {", 'rankdir="LR";', 'graph [bgcolor="transparent", pad="0.2"];',
             'node [shape="box", style="rounded,filled", fillcolor="#EAF1FB", color="#6B7FA3", fontname="Arial", fontsize="10"];',
             'edge [color="#7A8798", fontname="Arial", fontsize="9", arrowsize="0.7"];']
    for n in nodes:
        label = n["label"].replace("\\", "\\\\").replace('"', '\\"')
        if len(label) > 90: label = label[:87] + "..."
        color = "#F6C85F" if n["id"] == changed else ("#D5E8D4" if n["id"] in affected else "#EAF1FB")
        lines.append(f'"{n["id"]}" [label="{label}", fillcolor="{color}"];')
    for e in edges:
        label = e["mechanism"].replace('"', '\\"')
        if len(label) > 45: label = label[:42] + "..."
        lines.append(f'"{e["source"]}" -> "{e["target"]}" [label="{label}"];')
    return "\n".join(lines + ["}"])

def generate_branches(nodes: list[dict[str, str]], edges: list[dict[str, Any]], target: str,
                      intervention: str, decision: str, constraints: str, count: int) -> list[dict[str, Any]]:
    by_id = {n["id"]: n for n in nodes}
    affected = descendants(target, edges)
    outgoing = [e for e in edges if e["source"] == target]
    common = [{"step": 1, "claim": f"Baseline node: {by_id[target]['label']}", "basis": "User-defined or inferred node", "status": "Baseline"},
              {"step": 2, "claim": f"Intervention: {intervention}", "basis": "User-defined counterfactual", "status": "Counterfactual premise"}]
    for e in outgoing:
        common.append({"step": len(common)+1, "claim": f"{e['source']} connects to {e['target']} through {e['mechanism']} (strength: {e['strength']}).",
                       "basis": e["basis"], "status": "Graph dependency"})
    downstream = ", ".join(f"{by_id[i]['label']} [{i}]" for i in affected) if affected else "none encoded; add outgoing causal edges to trace propagation"
    common.append({"step": len(common)+1, "claim": f"Reachable downstream nodes: {downstream}.", "basis": "Graph reachability", "status": "Graph-derived"})
    results = []
    for i, (name, mechanism) in enumerate(LENSES[:count], 1):
        narrative = (f"Under the {name.lower()} lens, the intervention '{intervention}' changes the state represented by "
          f"'{by_id[target]['label']}'. Mechanism: {mechanism} The protagonist or system then reassesses "
          f"'{decision or 'the next consequential decision'}'. Potential downstream events are: {downstream}. "
          "Other actors may resist, compensate, or create new paths. This is a conditional hypothesis, not a guaranteed outcome. "
          f"Review it against these constraints: {constraints or 'preserve motivations, world rules, and chronology'}.")
        chain = common + [
          {"step": len(common)+1, "claim": f"Decision response at '{decision or 'the next consequential decision'}' under {name}: the decision may change, remain stable, or be delayed.", "basis": "Counterfactual hypothesis", "status": "Requires review"},
          {"step": len(common)+2, "claim": f"Outcome synthesis: {mechanism} Downstream effects depend on encoded edges and independent actor responses.", "basis": "Narrative synthesis over graph", "status": "Hypothesis"}]
        results.append({"id": i, "name": name, "mechanism": mechanism, "narrative": narrative,
          "affected_nodes": affected, "causal_chain": chain, "uncertainty": "Qualitative; not calibrated",
          "assumptions": ["The intervention occurs before the decision and can influence it.",
            "Graph edges encode plausible dependencies, not proof of causation.",
            "Unmodeled variables and independent actor choices may change the result.",
            constraints or "Preserve established motivations, world rules, and chronology."]})
    return results

def build_report(plot: str, nodes: list[dict[str, str]], edges: list[dict[str, Any]], target: str,
                 intervention: str, decision: str, constraints: str, branches: list[dict[str, Any]]) -> dict[str, Any]:
    return {"engine": "CANCE — Causal Analysis and Counterfactual Narrative Engine", "version": APP_VERSION,
      "generated_at_utc": datetime.now(timezone.utc).isoformat(), "baseline_plot": plot, "nodes": nodes, "causal_edges": edges,
      "intervention": {"node_id": target, "description": intervention}, "decision_point": decision,
      "preservation_constraints": constraints, "branches": branches,
      "method_note": "Reachability is computed from the directed graph. Counterfactual branches are qualitative hypotheses, not causal proof or calibrated predictions. Sentence-order fallback edges are provisional."}

def report_markdown(r: dict[str, Any]) -> str:
    out = ["# CANCE Causal Graph and Counterfactual Report", "", f"**Version:** {r['version']}",
      f"**Generated UTC:** {r['generated_at_utc']}", "", "## Baseline plot", r["baseline_plot"], "", "## Nodes"]
    out.extend(f"- **{n['id']}** — {n['label']} (type: {n['type']})" for n in r["nodes"])
    out += ["", "## Causal edges"]
    out.extend(f"- {e['source']} → {e['target']}: {e['mechanism']} (strength: {e['strength']}; basis: {e['basis']})" for e in r["causal_edges"])
    out += ["", "## Intervention", f"- Target: {r['intervention']['node_id']}", f"- Change: {r['intervention']['description']}",
      f"- Decision: {r['decision_point']}", f"- Constraints: {r['preservation_constraints']}", "", "## Method note", r["method_note"]]
    for b in r["branches"]:
        out += ["", f"## Outcome {b['id']}: {b['name']}", b["narrative"], "", "### Traceable chain"]
        out.extend(f"{s['step']}. {s['claim']} *(Basis: {s['basis']}; status: {s['status']})*" for s in b["causal_chain"])
        out += ["", "### Assumptions"] + [f"- {a}" for a in b["assumptions"]]
    return "\n".join(out) + "\n"

st.set_page_config(page_title="CANCE · Causal Graph Engine", page_icon="🕸️", layout="wide")
st.title("CANCE · Generic Causal Graph Engine")
st.caption("Model events and dependencies, intervene on a node, trace downstream effects, and generate alternative narratives.")
st.markdown("CANCE combines an editable causal graph with counterfactual narrative lenses. Keep baseline facts, intervention premises, graph-derived reachability, and speculative outcomes distinct.")

with st.sidebar:
    st.header("1 · Baseline")
    plot = st.text_area("Plot / system description", height=140, placeholder="Paste any plot, scenario, incident, or system description.")
    st.caption("Use the graph editor to override the provisional sentence-order graph.")
    default_nodes = "start | Initial situation | state\ndecision | Protagonist makes a choice | decision\nconsequence | Immediate consequence | event\noutcome | Downstream outcome | outcome"
    default_edges = "start -> decision | creates decision context | medium\ndecision -> consequence | action causes consequence | medium\nconsequence -> outcome | downstream dependency | unknown"
    nodes_raw = st.text_area("Nodes: id | label | type", value=default_nodes, height=135)
    edges_raw = st.text_area("Edges: source -> target | mechanism | strength", value=default_edges, height=135)
    st.caption("Strength is qualitative, not a probability.")
    st.header("2 · Intervention")
    target = st.text_input("Target node ID", value="decision")
    intervention = st.text_area("Counterfactual change", value="A crucial piece of information arrives before the decision.", height=90)
    decision = st.text_input("Decision point", value="the protagonist's next consequential choice")
    constraints = st.text_area("Character / system constraints", value="Preserve actor motivations, established world rules, chronology, and practical limits.", height=85)
    count = st.slider("Outcome branches", 3, 10, 5)
    use_inferred = st.checkbox("Infer provisional sentence chain if node editor is empty", value=True)
    run = st.button("Build graph & generate outcomes", type="primary", use_container_width=True)

if "cance_graph_report" not in st.session_state: st.session_state.cance_graph_report = None
if run:
    try:
        nodes = parse_nodes(nodes_raw)
        inferred = False
        if not nodes and use_inferred and (plot or "").strip():
            nodes, edges = infer_nodes_from_plot(plot)
            inferred = True
            if nodes and target not in {n["id"] for n in nodes}:
                target = nodes[0]["id"]
        else:
            edges = parse_edges(edges_raw, {n["id"] for n in nodes})
        errors = validate_graph(nodes, edges)
        if target not in {n["id"] for n in nodes}: errors.append(f"Intervention target '{target}' is not in the node list.")
        if not (intervention or "").strip(): errors.append("Describe the counterfactual intervention.")
        if errors:
            for error in errors: st.error(error)
        else:
            branches = generate_branches(nodes, edges, target, intervention, decision, constraints, count)
            st.session_state.cance_graph_report = build_report(plot, nodes, edges, target, intervention, decision, constraints, branches)
    except ValueError as exc:
        st.error(str(exc))

report = st.session_state.cance_graph_report
if report is None:
    st.subheader("Engine workflow")
    st.code("Plot / baseline → nodes and causal edges → do(intervention on node) → graph reachability → causal branch hypotheses → narrative synthesis", language="text")
    st.markdown("**Node format:** id | human-readable label | type\n\n**Edge format:** source_id -> target_id | causal mechanism | strength")
    st.info("Change the intervention target to a node ID that exists in the graph, such as decision. Replace sample nodes and edges to model your scenario.")
else:
    affected = set(descendants(report["intervention"]["node_id"], report["causal_edges"]))
    st.subheader("Causal graph")
    st.graphviz_chart(graph_dot(report["nodes"], report["causal_edges"], report["intervention"]["node_id"], affected), use_container_width=True)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Nodes", len(report["nodes"])); c2.metric("Causal edges", len(report["causal_edges"]))
    c3.metric("Reachable downstream nodes", len(affected)); c4.metric("Outcome branches", len(report["branches"]))
    with st.expander("Inspect graph data"): st.json({"nodes": report["nodes"], "edges": report["causal_edges"]})
    st.subheader("Intervention and affected subgraph")
    st.write(f"**Target:** {report['intervention']['node_id']} — {next(n['label'] for n in report['nodes'] if n['id'] == report['intervention']['node_id'])}")
    st.write(f"**Intervention:** {report['intervention']['description']}")
    if affected:
        for node_id in descendants(report["intervention"]["node_id"], report["causal_edges"]):
            node = next(n for n in report["nodes"] if n["id"] == node_id)
            st.markdown(f"- **{node_id} — {node['label']}**")
    else: st.info("No downstream nodes are reachable. Add outgoing edges if propagation is expected.")
    st.subheader("Counterfactual outcomes")
    st.warning("Reachability identifies modeled dependencies, not proven causal effects. Outcomes are hypotheses; no numeric probabilities are assigned.")
    for b in report["branches"]:
        with st.expander(f"{b['id']}. {b['name']}", expanded=(b["id"] == 1)):
            st.markdown("**Causal lens**"); st.write(b["mechanism"])
            st.markdown("**Alternative narrative**"); st.write(b["narrative"])
            st.markdown("**Traceable chain**")
            for s in b["causal_chain"]:
                st.markdown(f"**{s['step']}. {s['claim']}**"); st.caption(f"Basis: {s['basis']} · Status: {s['status']}")
            st.markdown("**Assumptions**")
            for a in b["assumptions"]: st.markdown(f"- {a}")
    st.subheader("Export")
    a,b = st.columns(2)
    a.download_button("Download Markdown report", report_markdown(report), file_name="cance_causal_counterfactual_report.md", mime="text/markdown", use_container_width=True)
    b.download_button("Download JSON graph + outcomes", json.dumps(report, ensure_ascii=False, indent=2), file_name="cance_causal_counterfactual_report.json", mime="application/json", use_container_width=True)
    st.caption(f"CANCE v{APP_VERSION} · Inspect graph edges before interpreting outcomes.")
st.divider()
st.caption("This prototype uses explicit graph edges and an optional sentence-order fallback. It is auditable scaffolding, not automated causal discovery.")
