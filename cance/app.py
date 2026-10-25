from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

import streamlit as st

APP_VERSION = "0.2.0"

LENSES = [
    {"name": "Information arrives earlier", "mechanism": "Belief revision", "focus": "new information changes what the protagonist knows"},
    {"name": "A hidden option becomes available", "mechanism": "Feasible-set expansion", "focus": "the protagonist sees a practical alternative"},
    {"name": "An alliance changes", "mechanism": "Trust and coordination", "focus": "a relationship changes access to support or resistance"},
    {"name": "A key resource changes", "mechanism": "Resource constraint", "focus": "time, money, evidence, power, or capacity changes"},
    {"name": "A choice is delayed", "mechanism": "Timing and commitment", "focus": "delay creates new information but also new costs"},
    {"name": "A plan partially fails", "mechanism": "Feedback and adaptation", "focus": "an unexpected setback forces a response"},
    {"name": "An opponent adapts", "mechanism": "Strategic response", "focus": "another actor reacts to the intervention"},
    {"name": "The protagonist refuses the expected choice", "mechanism": "Agency and value conflict", "focus": "the protagonist prioritizes a different value"},
    {"name": "A chance event changes", "mechanism": "Contingency", "focus": "an external event changes the opportunity or risk"},
    {"name": "A small decision compounds", "mechanism": "Path dependence", "focus": "an early difference accumulates into larger consequences"},
]

def clean(text: str, fallback: str) -> str:
    value = " ".join((text or "").split())
    return value if value else fallback

def make_branches(plot: str, decision: str, intervention: str, character_rules: str,
                  world_rules: str, count: int, tone: str) -> list[dict[str, Any]]:
    plot = clean(plot, "The supplied story")
    decision = clean(decision, "the next consequential decision")
    intervention = clean(intervention, "one consequential condition changes before the decision")
    character_rules = clean(character_rules, "Keep established motivations, knowledge, and personality plausible.")
    world_rules = clean(world_rules, "Keep the story world's established rules and practical constraints.")
    results = []
    for i, lens in enumerate(LENSES[:count], 1):
        intervention_line = intervention if i == 1 else f"{intervention}. Explore this through the lens of {lens['focus']}."
        chain = [
            {"step": 1, "label": "Baseline", "claim": f"Before the intervention, the plot is constrained by its established setup: {plot[:420]}", "basis": "User-supplied plot", "status": "Provided"},
            {"step": 2, "label": "Intervention", "claim": intervention_line, "basis": "User-selected what-if", "status": "Counterfactual premise"},
            {"step": 3, "label": "Mechanism", "claim": f"The intervention operates through {lens['mechanism'].lower()}: {lens['focus']}.", "basis": "Causal hypothesis", "status": "Inferred"},
            {"step": 4, "label": "Decision response", "claim": f"At the decision point ({decision}), the protagonist reassesses available actions in light of the changed condition. The response is not assumed to be automatic.", "basis": "Decision model", "status": "Hypothesis"},
            {"step": 5, "label": "Immediate consequence", "claim": f"The selected action changes at least one immediate consequence: who knows what, which options remain open, who cooperates, or what cost is incurred.", "basis": "Mechanism-dependent implication", "status": "Hypothesis"},
            {"step": 6, "label": "Downstream propagation", "claim": f"Other characters and external conditions respond to the changed state; their reactions may amplify, dampen, or reverse the initial effect.", "basis": "Interaction and feedback", "status": "Hypothesis"},
            {"step": 7, "label": "Outcome", "claim": f"A {tone.lower()} alternative trajectory emerges, conditional on the assumptions below—not a guaranteed result.", "basis": "Counterfactual synthesis", "status": "Generated"},
        ]
        results.append({
            "id": i, "title": f"Outcome {i}: {lens['name']}", "mechanism": lens["mechanism"],
            "causal_focus": lens["focus"], "intervention": intervention_line, "chain": chain,
            "narrative": (
                f"In this branch of the story, {intervention_line}. At {decision}, the protagonist "
                f"responds through {lens['mechanism'].lower()} rather than simply following the original path. "
                f"The first change affects the immediate choice; that choice then alters the information, "
                f"relationships, resources, or risks available to the next scene. As other characters react, "
                f"the consequences propagate and may create a second conflict. The resulting {tone.lower()} "
                f"trajectory is therefore different from the baseline, but not necessarily easier or happier. "
                f"The ending should follow from the chain rather than be imposed independently."
            ),
            "assumptions": [
                f"The intervention occurs early enough to influence {decision}.",
                character_rules,
                world_rules,
                "Other characters retain independent goals and may resist, misunderstand, or counter the change.",
                "Only consequences supported by the chain should be treated as plausible; unmodeled events remain uncertain.",
            ],
            "uncertainty": "Qualitative; not calibrated",
            "checks": {
                "Minimal change": "The branch changes the specified premise, not the entire story world.",
                "Character continuity": character_rules,
                "World consistency": world_rules,
                "Causal traceability": "Each major outcome should be traceable to a prior step in this chain.",
            },
        })
    return results

def build_report(plot: str, decision: str, intervention: str, character_rules: str,
                 world_rules: str, tone: str, branches: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "engine": "CANCE — Causal Analysis and Narrative Counterfactual Engine",
        "version": APP_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input": {"plot": plot, "decision_point": decision, "intervention": intervention,
                  "character_preservation": character_rules, "world_constraints": world_rules, "tone": tone},
        "branches": branches,
        "method": {
            "approach": "Structured, rule-based causal scaffolding",
            "evidence_policy": "User-provided plot is the baseline; interventions and generated consequences are counterfactual hypotheses.",
            "probabilities": "No numeric probabilities are assigned.",
            "limitation": "This version creates structured drafts from user inputs. It does not independently verify source material or use a language model to deeply interpret the plot.",
        },
    }

def report_markdown(report: dict[str, Any]) -> str:
    out = ["# CANCE Counterfactual Analysis", "", f"**Version:** {report['version']}",
           f"**Generated UTC:** {report['generated_at_utc']}", "", "## Scenario inputs",
           f"**Plot:** {report['input']['plot']}", f"**Decision point:** {report['input']['decision_point']}",
           f"**Intervention:** {report['input']['intervention']}",
           f"**Character constraints:** {report['input']['character_preservation']}",
           f"**World constraints:** {report['input']['world_constraints']}", f"**Tone:** {report['input']['tone']}",
           "", "## Method and limitations", report["method"]["limitation"],
           "Generated branches are hypotheses, not canonical facts. No numeric probabilities are assigned."]
    for b in report["branches"]:
        out += ["", f"## {b['title']}", f"**Mechanism:** {b['mechanism']}",
                f"**Causal focus:** {b['causal_focus']}", "", "### Alternative narrative", b["narrative"], "",
                "### Traceable causal chain"]
        out.extend([f"{s['step']}. **{s['label']}** — {s['claim']} *(Basis: {s['basis']}; {s['status']})*" for s in b["chain"]])
        out += ["", "### Assumptions"] + [f"- {a}" for a in b["assumptions"]]
        out += ["", "### Consistency checks"] + [f"- **{k}:** {v}" for k, v in b["checks"].items()]
    return "\n".join(out) + "\n"

st.set_page_config(page_title="CANCE · Narrative Engine", page_icon="🧭", layout="wide")
st.title("CANCE · Causal Counterfactual Narrative Engine")
st.caption("Turn any plot into multiple alternative outcomes with traceable causal chains.")
st.markdown("Paste a plot or synopsis, choose a decision point and a what-if intervention, then inspect how each proposed outcome follows from explicit causal steps. The engine labels assumptions and distinguishes your baseline from invented alternatives.")

with st.sidebar:
    st.header("1 · Story and intervention")
    plot = st.text_area("Plot / synopsis", height=210, placeholder="Paste a story summary, screenplay scene, game quest, or scenario.")
    decision = st.text_input("Key decision or turning point", placeholder="e.g., The lead decides whether to reveal the evidence")
    intervention = st.text_area("What changes in the counterfactual?", height=100, placeholder="e.g., The evidence reaches the lead one day earlier")
    st.header("2 · Constraints")
    character_rules = st.text_area("Character / protagonist constraints", value="Preserve established goals, personality, knowledge, and believable emotional reactions.", height=85)
    world_rules = st.text_area("World / plot constraints", value="Respect established world rules, chronology, resources, and consequences.", height=85)
    tone = st.selectbox("Outcome tone", ["Balanced", "Hopeful", "Tragic", "Suspenseful", "Ambiguous", "Realistic"])
    count = st.slider("Number of outcomes", min_value=3, max_value=10, value=5)
    generate = st.button("Generate counterfactual outcomes", type="primary", use_container_width=True)

if "cance_report" not in st.session_state:
    st.session_state.cance_report = None

if generate:
    if len((plot or "").strip()) < 30:
        st.error("Please enter a plot or synopsis of at least 30 characters.")
    elif not (intervention or "").strip():
        st.error("Describe the counterfactual intervention first.")
    else:
        branches = make_branches(plot, decision, intervention, character_rules, world_rules, count, tone)
        st.session_state.cance_report = build_report(plot, decision, intervention, character_rules, world_rules, tone, branches)

report = st.session_state.cance_report
if report is None:
    st.info("Start by entering a plot, a turning point, and one change. The engine will produce several alternative branches and show the causal steps behind each.")
    st.subheader("How traceability works")
    st.code("Baseline plot → Intervention → Causal mechanism → Decision response → Immediate consequence → Feedback from others → Alternative outcome", language="text")
    st.markdown("**Example intervention:** a key witness tells the protagonist the truth before the confrontation. The engine explores how that information could change the decision and how later characters and events respond.")
else:
    st.subheader("Scenario overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Alternative outcomes", len(report["branches"]))
    c2.metric("Causal steps per outcome", 7)
    c3.metric("Numeric probabilities", "Not assigned")
    st.warning("Generated outcomes are conditional hypotheses, not facts or predictions. The current engine uses structured rules rather than a connected LLM.")
    with st.expander("Baseline and intervention", expanded=True):
        st.markdown("**Original plot / baseline**")
        st.write(report["input"]["plot"])
        st.markdown("**Decision point**")
        st.write(report["input"]["decision_point"] or "Not specified; refine this for a more precise causal model.")
        st.markdown("**Counterfactual intervention**")
        st.write(report["input"]["intervention"])
    st.subheader("Alternative outcomes")
    for branch in report["branches"]:
        with st.expander(f"{branch['id']}. {branch['title']} · {branch['mechanism']}", expanded=(branch["id"] == 1)):
            st.markdown("**Narrative outcome**")
            st.write(branch["narrative"])
            st.markdown("**Causal chain — inspect every link**")
            for step in branch["chain"]:
                st.markdown(f"**{step['step']}. {step['label']}**")
                st.write(step["claim"])
                st.caption(f"Basis: {step['basis']} · Status: {step['status']}")
            st.markdown("**Assumptions that must hold**")
            for item in branch["assumptions"]:
                st.markdown(f"- {item}")
            st.markdown("**Consistency and traceability checks**")
            for name, description in branch["checks"].items():
                st.markdown(f"- **{name}:** {description}")
    st.subheader("Export")
    md = report_markdown(report)
    js = json.dumps(report, ensure_ascii=False, indent=2)
    a, b = st.columns(2)
    a.download_button("Download Markdown report", md, file_name="cance_counterfactual_report.md", mime="text/markdown", use_container_width=True)
    b.download_button("Download JSON data", js, file_name="cance_counterfactual_report.json", mime="application/json", use_container_width=True)
    st.caption(f"CANCE prototype v{APP_VERSION}. Review the causal chain manually; the labels are qualitative and are not calibrated probabilities.")
