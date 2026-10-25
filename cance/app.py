from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

import streamlit as st

APP_VERSION = "0.1.0"

BRANCHES: list[dict[str, Any]] = [
    {
        "id": 1,
        "name": "The truth about Vijayendra arrives early",
        "mechanism": "Belief revision",
        "intervention": "A trusted person shares credible information about Vijayendra's expectations, commitments, or capacity to offer the future Zubeidaa wants.",
        "causal_chain": [
            "A consequential disclosure reaches Zubeidaa before commitment.",
            "She revises or tests her beliefs about the relationship.",
            "The perceived emotional and practical costs of commitment change.",
            "She confronts the information and weighs it against her attachment.",
            "She delays, renegotiates, refuses, or proceeds with greater awareness."
        ],
        "response": "She questions the source and meaning of the information rather than automatically accepting it. Her attachment and desire for a meaningful life remain active motives.",
        "ending": "She may postpone or refuse the commitment, or proceed while understanding its costs. A tragic ending remains possible if attachment or external constraints outweigh the warning.",
        "themes": "The difference between knowing the cost of a choice and being able to bear the cost of refusing it; love, knowledge, and constraint.",
        "assumptions": [
            "The disclosure is credible and relevant to a decision not yet made.",
            "Zubeidaa has a meaningful opportunity to act on it.",
            "Her underlying attachments and aspirations remain intact."
        ],
        "uncertainty": "High",
        "uncertainty_reason": "The effect depends on the disclosure's exact content, credibility, and interpretation."
    },
    {
        "id": 2,
        "name": "A trusted person reveals overlooked alternatives",
        "mechanism": "Feasible-set expansion",
        "intervention": "A trusted person explains a practical alternative that could preserve some independence or artistic ambition.",
        "causal_chain": [
            "A confidant describes a concrete alternative path.",
            "Zubeidaa recognizes that the choice is not as binary as she thought.",
            "The perceived feasible set expands, subject to real resources and constraints.",
            "She considers a path that preserves more of her agency.",
            "She negotiates, delays, or pursues an alternative, potentially at a cost."
        ],
        "response": "She tries to preserve what matters to her without suddenly becoming detached or calculating. She tests whether the proposed alternative is genuinely feasible.",
        "ending": "She may establish greater independence while retaining some relationships or artistic identity. Social, financial, and emotional costs may remain.",
        "themes": "Agency, social constraint, and the way a narrow view of available choices can make an outcome appear inevitable.",
        "assumptions": [
            "The alternative is practically feasible, not merely imaginable.",
            "Zubeidaa has enough time, support, or resources to pursue it.",
            "The trusted person offers actionable information."
        ],
        "uncertainty": "Moderate–high",
        "uncertainty_reason": "The information expands perceived options, but external constraints may make those options unavailable in practice."
    },
    {
        "id": 3,
        "name": "A confidant discloses a relational conflict",
        "mechanism": "Trust and coordination",
        "intervention": "A trusted person discloses a significant conflict or incompatible expectation before Zubeidaa makes a consequential decision.",
        "causal_chain": [
            "A confidant shares information about a developing relational conflict.",
            "Zubeidaa revises her interpretation of the situation.",
            "She asks direct questions or seeks clarification.",
            "The other people involved respond with honesty, denial, repair, or escalation.",
            "Trust is restored, renegotiated, or broken, changing the next decision."
        ],
        "response": "She addresses the conflict directly and emotionally, while retaining her need for attachment and agency.",
        "ending": "The relationship may continue on revised terms, or Zubeidaa may separate earlier and more deliberately. Neither reconciliation nor separation is guaranteed.",
        "themes": "Relationships as information networks; concealment, interpretation, trust, and the limits of repair.",
        "assumptions": [
            "The disclosure is accurate rather than malicious gossip.",
            "The conflict is still negotiable when revealed.",
            "The people involved can respond meaningfully."
        ],
        "uncertainty": "High",
        "uncertainty_reason": "The disclosure changes what Zubeidaa knows, but other characters' reactions introduce additional causal uncertainty."
    },
    {
        "id": 4,
        "name": "Riyaz shares his perspective before the choice",
        "mechanism": "Competing perspectives and deliberation",
        "intervention": "In this hypothetical branch, Riyaz shares relevant knowledge from their shared history before Zubeidaa commits to a consequential choice.",
        "causal_chain": [
            "Riyaz communicates a perspective or consequence Zubeidaa has not fully considered.",
            "She compares his account with her own understanding.",
            "She evaluates immediate emotional needs alongside longer-term aspirations.",
            "She challenges or accepts parts of his interpretation while retaining agency.",
            "She delays, changes, or reaffirms her decision with a different understanding."
        ],
        "response": "She listens but does not automatically let Riyaz decide for her. Her response remains shaped by her own attachments, ambitions, and judgement.",
        "ending": "She may make a more deliberate choice, including a choice that still involves separation or continued attachment to Vijayendra. Later understanding may still arrive too late to undo consequences.",
        "themes": "The timing of understanding, retrospective knowledge, and the difference between being understood and being free to choose.",
        "assumptions": [
            "Riyaz has relevant information and an opportunity to share it.",
            "Zubeidaa considers his perspective sufficiently trustworthy.",
            "The decision is still reversible or influenceable."
        ],
        "uncertainty": "High",
        "uncertainty_reason": "Both the content of the information and Zubeidaa's interpretation of Riyaz's involvement matter."
    },
    {
        "id": 5,
        "name": "A trusted person warns her before the final journey",
        "mechanism": "Risk reassessment",
        "intervention": "Before a consequential journey, a trusted person communicates credible, actionable information about a relevant risk or unresolved concern.",
        "causal_chain": [
            "A specific warning reaches Zubeidaa before the journey decision.",
            "She revises her assessment of the risk, depending on the warning's credibility.",
            "She considers delaying, checking the information, changing arrangements, or proceeding.",
            "She weighs the warning against her intentions, attachments, and constraints.",
            "The journey's timing or circumstances may change—or remain unchanged."
        ],
        "response": "She evaluates the warning in context; she is not assumed to become perfectly rational or to disregard her relationships.",
        "ending": "She might delay or avoid the journey, changing the immediate trajectory. Survival or a happy ending cannot be inferred; other risks and conflicts remain.",
        "themes": "Foreseeability versus preventability, knowledge versus control, and the danger of assuming a tragedy could certainly have been avoided.",
        "assumptions": [
            "The warning is specific, credible, and available in time.",
            "Zubeidaa can reasonably act on it.",
            "The warning is relevant to the actual risk."
        ],
        "uncertainty": "Very high",
        "uncertainty_reason": "The warning and its causal relevance are hypothetical; the narrative does not justify numerical survival or accident-avoidance probabilities."
    },
]

ESTABLISHED_FACTS = [
    "Zubeidaa has artistic ambitions and experiences conflict with family expectations.",
    "Her relationships and marriage into a royal household are central to the narrative.",
    "The story explores personal desire, attachment, social constraint, and agency.",
    "Riyaz's retrospective investigation provides a frame for reconstructing her life."
]

INVENTED_EVENTS = [
    "Each branch's early disclosure is invented for analysis and is not asserted to be a hidden scene in the film.",
    "The exact content, source, and timing of each disclosure are hypothetical.",
    "All alternative decisions and endings are counterfactual, not canonical.",
    "No specific preventable warning, mechanical defect, or definitive causal explanation for the final flight is assumed."
]

PRESERVATION_TESTS = [
    ("Motivational continuity", "Does Zubeidaa retain recognizable ambitions, attachments, and needs?"),
    ("Information credibility", "Could she plausibly receive and evaluate this disclosure?"),
    ("Decision sensitivity", "Is there an explicit mechanism by which the information changes—or reaffirms—her choice?"),
    ("Constraint realism", "Do social, emotional, and practical barriers remain visible?"),
    ("Consequence traceability", "Can major outcomes be traced back through explicit causal steps?")
]


def build_report(
    selected: list[dict[str, Any]],
    intervention_text: str,
    preservation: dict[str, bool],
    notes: str,
) -> dict[str, Any]:
    return {
        "framework": "CANCE — Causal Analysis and Narrative Counterfactual Engine",
        "version": APP_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "story": "Zubeidaa (2001)",
        "intervention_type": "Relationship-mediated information",
        "user_intervention": intervention_text,
        "preservation_constraint": "Character identity and motivational continuity",
        "established_story_facts": ESTABLISHED_FACTS,
        "invented_counterfactual_events_and_caveats": INVENTED_EVENTS,
        "preservation_checks": preservation,
        "analyst_notes": notes,
        "branches": selected,
        "method_note": (
            "Qualitative causal hypotheses only. No empirical probabilities are assigned. "
            "A disclosure does not logically guarantee a changed decision or outcome."
        ),
    }


def to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# CANCE Counterfactual Narrative Report",
        "",
        f"**Story:** {report['story']}",
        f"**Framework version:** {report['version']}",
        f"**Generated (UTC):** {report['generated_at_utc']}",
        f"**Intervention:** {report['user_intervention']}",
        "",
        "## Method and caveats",
        report["method_note"],
        "",
        "## Established story facts",
    ]
    lines.extend(f"- {item}" for item in report["established_story_facts"])
    lines += ["", "## Invented events and boundaries"]
    lines.extend(f"- {item}" for item in report["invented_counterfactual_events_and_caveats"])
    lines += ["", "## Character-preservation checks"]
    lines.extend(
        f"- {'[x]' if passed else '[ ]'} **{name}:** {passed}"
        for name, passed in report["preservation_checks"].items()
    )
    if report["analyst_notes"]:
        lines += ["", "## Analyst notes", report["analyst_notes"]]
    for branch in report["branches"]:
        lines += [
            "",
            f"## Branch {branch['id']}: {branch['name']}",
            f"**Mechanism:** {branch['mechanism']}",
            "",
            f"**Intervention:** {branch['intervention']}",
            "",
            "**Causal chain:**",
        ]
        lines.extend(f"{i}. {step}" for i, step in enumerate(branch["causal_chain"], 1))
        lines += [
            "",
            f"**Character response:** {branch['response']}",
            "",
            f"**Counterfactual ending:** {branch['ending']}",
            "",
            f"**Thematic implications:** {branch['themes']}",
            "",
            "**Assumptions:**",
        ]
        lines.extend(f"- {item}" for item in branch["assumptions"])
        lines += [
            "",
            f"**Uncertainty:** {branch['uncertainty']}",
            branch["uncertainty_reason"],
        ]
    return "\n".join(lines) + "\n"


st.set_page_config(page_title="CANCE Narrative Engine", page_icon="🧭", layout="wide")
st.title("CANCE · Counterfactual Narrative Engine")
st.caption("Causal what-if analysis with character-preservation constraints")
st.markdown(
    "Explore how a relationship-mediated disclosure could change a character's beliefs, "
    "choices, and downstream story trajectory—without treating hypothetical events as film facts."
)

with st.sidebar:
    st.header("Scenario controls")
    story = st.text_input("Story", value="Zubeidaa (2001)")
    intervention_text = st.text_area(
        "Counterfactual intervention",
        value="The protagonist receives crucial information through a relationship before making the decision.",
        height=110,
    )
    selected_ids = st.multiselect(
        "Branches to include",
        options=[b["id"] for b in BRANCHES],
        default=[1, 2, 3, 4, 5],
        format_func=lambda i: f"{i}. {BRANCHES[i - 1]['name']}",
    )
    st.divider()
    st.subheader("Character preservation")
    preservation = {}
    for name, prompt in PRESERVATION_TESTS:
        preservation[name] = st.checkbox(name, value=True, help=prompt)
    analyst_notes = st.text_area("Analyst notes (optional)", placeholder="Record scene-level evidence or interpretation caveats.")

if story.strip().lower() not in {"zubeidaa", "zubeidaa (2001)"}:
    st.info("This build is preloaded with Zubeidaa. Other stories can be entered for notes, but branch content remains specific to Zubeidaa.")

selected = [b for b in BRANCHES if b["id"] in selected_ids]
report = build_report(selected, intervention_text.strip(), preservation, analyst_notes.strip())
report["story"] = story.strip() or "Zubeidaa (2001)"

metric_cols = st.columns(3)
metric_cols[0].metric("Branches selected", len(selected))
metric_cols[1].metric("Preservation checks passed", f"{sum(preservation.values())}/{len(preservation)}")
metric_cols[2].metric("Numeric probabilities", "Not assigned")

st.subheader("Baseline: established facts")
st.markdown("These are broad story elements used as the baseline, not a scene-by-scene verified annotation.")
for fact in ESTABLISHED_FACTS:
    st.markdown(f"- {fact}")

with st.expander("What is invented in this analysis?", expanded=True):
    for fact in INVENTED_EVENTS:
        st.markdown(f"- {fact}")

st.subheader("Causal model")
st.code(
    "Relationship disclosure\n"
    "        ↓\n"
    "Belief / perceived options / risk assessment changes\n"
    "        ↓\n"
    "Character-consistent decision process\n"
    "        ↓\n"
    "Changed or reaffirmed action\n"
    "        ↓\n"
    "Alternative downstream trajectory",
    language="text",
)
st.caption(
    "Formal shorthand: X[t+1] = F(X[t], A[t], W[t]); intervention do(I[t] = i). "
    "Belief change does not guarantee a decision change; decision change does not guarantee an outcome change."
)

st.subheader("Counterfactual branches")
if not selected:
    st.warning("Select at least one branch in the sidebar.")
for branch in selected:
    with st.expander(f"Branch {branch['id']} · {branch['name']} · Uncertainty: {branch['uncertainty']}", expanded=(branch["id"] == 1)):
        st.markdown(f"**Primary mechanism:** {branch['mechanism']}")
        st.markdown("**Intervention**")
        st.write(branch["intervention"])
        st.markdown("**Causal chain**")
        for i, step in enumerate(branch["causal_chain"], 1):
            st.markdown(f"{i}. {step}")
        st.markdown("**Character response**")
        st.write(branch["response"])
        st.markdown("**Counterfactual ending**")
        st.write(branch["ending"])
        st.markdown("**Thematic implications**")
        st.write(branch["themes"])
        st.markdown("**Assumptions**")
        for assumption in branch["assumptions"]:
            st.markdown(f"- {assumption}")
        st.markdown(f"**Uncertainty: {branch['uncertainty']}**")
        st.write(branch["uncertainty_reason"])

st.subheader("Character-preservation review")
for name, prompt in PRESERVATION_TESTS:
    status = "Pass" if preservation[name] else "Needs review"
    st.markdown(f"- **{status} — {name}:** {prompt}")

st.subheader("Export report")
st.write("Export the selected branches, baseline facts, invented-event caveats, preservation checks, and uncertainty notes.")
md_report = to_markdown(report)
json_report = json.dumps(report, ensure_ascii=False, indent=2)
download_cols = st.columns(2)
download_cols[0].download_button(
    "Download Markdown report",
    data=md_report,
    file_name="cance_zubeidaa_counterfactual_report.md",
    mime="text/markdown",
    use_container_width=True,
)
download_cols[1].download_button(
    "Download JSON data",
    data=json_report,
    file_name="cance_zubeidaa_counterfactual_report.json",
    mime="application/json",
    use_container_width=True,
)

st.divider()
st.caption(
    f"CANCE prototype v{APP_VERSION}. Interpretive tool, not a validated predictive model. "
    "No empirical probabilities or definitive claims about the film's final flight are inferred."
)
