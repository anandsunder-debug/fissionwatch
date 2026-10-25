from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from itertools import combinations
from typing import Any

import streamlit as st

APP_VERSION = "0.4.0"

GENRES = ["Drama", "Thriller", "Science fiction", "Mystery", "Romance", "Comedy", "Adventure", "Horror", "Political", "Fantasy"]
TONES = ["Balanced", "Hopeful", "Dark", "Suspenseful", "Ambiguous", "Satirical", "Emotional", "Realistic"]
VARIATIONS = [
    {"name": "Information reveal", "tag": "knowledge", "move": "A character discovers a consequential fact earlier than expected.", "turn": "The new information changes what the lead believes, but not what they can immediately control.", "ending": "The truth resolves one uncertainty and exposes a more difficult choice."},
    {"name": "Ally turns", "tag": "relationship", "move": "An ally with an independent goal refuses the expected role and makes a costly counteroffer.", "turn": "The protagonist must renegotiate trust instead of relying on the original alliance.", "ending": "The relationship survives in a changed form, or its rupture forces a new coalition."},
    {"name": "Resource constraint", "tag": "constraint", "move": "A deadline, scarce resource, or practical limitation removes the easiest solution.", "turn": "The lead must choose which value to protect and which cost to accept.", "ending": "The immediate goal may be reached, but a visible trade-off remains."},
    {"name": "Moral reversal", "tag": "values", "move": "The apparent solution would harm someone the protagonist has overlooked.", "turn": "The lead revises the plan after confronting the human cost of success.", "ending": "The protagonist earns a more difficult, morally legible victory or accepts a loss."},
    {"name": "Opponent adapts", "tag": "strategy", "move": "The antagonist recognizes the plan and changes tactics instead of waiting passively.", "turn": "The protagonist's first advantage becomes a new vulnerability.", "ending": "The conflict shifts from a direct contest to a test of adaptation."},
    {"name": "Small choice compounds", "tag": "path-dependence", "move": "A seemingly minor early decision creates a consequence that returns later.", "turn": "The lead recognizes the link between an earlier compromise and the current crisis.", "ending": "The final choice pays off the earlier setup rather than relying on coincidence."},
    {"name": "Unexpected cooperation", "tag": "coalition", "move": "Two rivals cooperate temporarily because their goals overlap, without abandoning their differences.", "turn": "The shared plan succeeds only while both sides keep negotiating their limits.", "ending": "The immediate danger changes, but the unresolved disagreement seeds a sequel or final dilemma."},
    {"name": "Failure and adaptation", "tag": "feedback", "move": "The first plan fails in a way that reveals a flaw in the protagonist's model of the problem.", "turn": "The lead updates the strategy using evidence from the failure.", "ending": "The revised plan succeeds, partially succeeds, or reveals a deeper cost."},
    {"name": "Perspective shift", "tag": "perspective", "move": "A secondary character reveals how the central conflict looks from outside the protagonist's assumptions.", "turn": "The lead must test their interpretation rather than simply switch sides.", "ending": "The conflict becomes more complex, and the resolution reflects a changed understanding."},
    {"name": "Reversal with a price", "tag": "sacrifice", "move": "The protagonist gains leverage but must sacrifice something established as important.", "turn": "The lead weighs the external objective against an internal value.", "ending": "The climax delivers a consequential win, loss, or ambiguous exchange."},
]

def words(text: str) -> set[str]:
    return {w.lower() for w in re.findall(r"[A-Za-z0-9']+", text) if len(w) > 3}

def similarity(a: str, b: str) -> float:
    wa, wb = words(a), words(b)
    return len(wa & wb) / max(1, len(wa | wb))

def build_candidates(title: str, premise: str, protagonist: str, goal: str, stakes: str,
                     constraints: str, genre: str, tone: str, scene_count: int,
                     candidate_count: int) -> list[dict[str, Any]]:
    candidates = []
    for i in range(candidate_count):
        variation = VARIATIONS[i % len(VARIATIONS)]
        # Rotate the sequence to produce materially different causal paths.
        second = VARIATIONS[(i + 3) % len(VARIATIONS)]
        third = VARIATIONS[(i + 6) % len(VARIATIONS)]
        beats = [
            {"scene": 1, "purpose": "Setup", "event": f"Establish {protagonist}, their immediate world, and the central tension in: {premise}", "causal_link": "The opening establishes the baseline state and what can be lost."},
            {"scene": 2, "purpose": "Goal and stakes", "event": f"{protagonist} pursues {goal}. The cost of failure is made concrete: {stakes}.", "causal_link": "The goal and stakes make later choices consequential."},
            {"scene": 3, "purpose": "Inciting disruption", "event": f"{variation['move']} This disrupts the original plan.", "causal_link": f"Variation mechanism: {variation['tag']}. The disruption narrows or changes the feasible choices."},
            {"scene": 4, "purpose": "First response", "event": f"{protagonist} tries to regain control, but {second['move'].lower()}", "causal_link": f"The response creates a second-order effect through {second['tag']}."},
            {"scene": 5, "purpose": "Midpoint reversal", "event": f"{third['move']} The apparent route to success becomes more complicated.", "causal_link": f"The {third['tag']} mechanism forces the protagonist to update their plan."},
            {"scene": 6, "purpose": "Crisis and decision", "event": f"Under pressure, {protagonist} must choose between the goal ({goal}) and a competing value or relationship. {variation['turn']}", "causal_link": "The crisis resolves from the prior setup and the accumulated costs, not from an unrelated coincidence."},
            {"scene": 7, "purpose": "Climax", "event": f"The protagonist acts on the decision. The opposing force reacts, and the consequences of the choice become visible.", "causal_link": "The climax tests the decision against the story's established stakes."},
            {"scene": 8, "purpose": "Resolution", "event": f"{variation['ending']} The final image reflects the cost of the choice and leaves a distinct emotional aftertaste.", "causal_link": "The resolution pays off the selected causal path and preserves consequences."},
        ]
        beats = beats[:max(4, min(8, scene_count))]
        labels = [variation["tag"], second["tag"], third["tag"]]
        script = "\n\n".join(f"SCENE {b['scene']} — {b['purpose'].upper()}\n{b['event']}\nCausal function: {b['causal_link']}" for b in beats)
        candidates.append({
            "id": i + 1,
            "title": f"{title.strip() or 'Untitled Film'} — Variation {i + 1}: {variation['name']}",
            "genre": genre, "tone": tone, "variation": variation["name"],
            "variation_tags": labels, "premise": premise, "protagonist": protagonist,
            "goal": goal, "stakes": stakes, "constraints": constraints,
            "beats": beats, "script_draft": script,
            "logline": f"When {premise.strip().rstrip('.')}, {protagonist} must {goal}, or risk {stakes}. A {variation['name'].lower()} forces a choice that changes the route to the climax.",
            "causal_summary": f"{variation['tag']} disrupts the baseline → {second['tag']} complicates the response → {third['tag']} reshapes the midpoint → decision under cost → consequence-based resolution.",
        })
    return candidates

def score_candidate(candidate: dict[str, Any], all_candidates: list[dict[str, Any]],
                    weights: dict[str, float], constraints: str) -> dict[str, Any]:
    text = candidate["script_draft"]
    # Transparent heuristic proxies, not learned or audience-validated scores.
    causal = 8.0 if all(b.get("causal_link") for b in candidate["beats"]) else 3.0
    character = 7.0 if candidate["protagonist"].strip() and candidate["goal"].strip() else 3.0
    variation = 6.0 + min(3.0, len(set(candidate["variation_tags"])) * 0.7)
    specificity = min(9.0, 4.0 + min(5.0, len(words(candidate["premise"])) / 8))
    payoff = 7.5 if len(candidate["beats"]) >= 6 else 5.5
    constraint_score = 7.0 if constraints.strip() else 5.0
    components = {
        "Causal coherence": causal,
        "Character / goal continuity": character,
        "Variation capture": variation,
        "Premise specificity": specificity,
        "Payoff structure": payoff,
        "Constraint adherence (proxy)": constraint_score,
    }
    total_weight = sum(max(0.0, weights.get(k, 0.0)) for k in components)
    reward = sum(components[k] * max(0.0, weights.get(k, 0.0)) for k in components) / total_weight if total_weight else 0.0
    candidate["utility_components"] = components
    candidate["reward_score"] = round(reward, 2)
    candidate["reward_formula"] = "U = sum(w_i * q_i) / sum(w_i); q_i are transparent heuristic proxies on a 0–10 scale."
    candidate["reward_caveat"] = "Prototype heuristic reward only. It is not an audience preference estimate, learned reward model, or validated quality metric."
    return candidate

def score_diversity(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    pairs = []
    for a, b in combinations(candidates, 2):
        sim = similarity(a["script_draft"], b["script_draft"])
        pairs.append({"a": a["id"], "b": b["id"], "similarity": round(sim, 3), "variation_distance": round(1-sim, 3)})
    mean_sim = sum(p["similarity"] for p in pairs) / len(pairs) if pairs else 0.0
    unique_tags = sorted({tag for c in candidates for tag in c["variation_tags"]})
    return {"pairwise": pairs, "mean_text_similarity": round(mean_sim, 3),
            "variation_coverage": unique_tags, "variation_coverage_count": len(unique_tags),
            "interpretation": "Lexical Jaccard similarity is a rough variation signal; it does not measure semantic originality or narrative quality."}

def make_report(inputs: dict[str, Any], candidates: list[dict[str, Any]], diversity: dict[str, Any]) -> dict[str, Any]:
    return {"engine": "CANCE Movie Generator — causal branching with reward-based utility and variation capture",
            "version": APP_VERSION, "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "inputs": inputs, "reward_model": {"formula": "U = sum(w_i * q_i) / sum(w_i)",
            "meaning": "Weighted heuristic utility; q_i are transparent 0–10 proxies, not validated ratings."},
            "diversity_analysis": diversity, "candidates": candidates}

def markdown_report(report: dict[str, Any]) -> str:
    out = ["# CANCE Movie Generator Report", "", f"Version: {report['version']}",
           f"Generated UTC: {report['generated_at_utc']}", "", "## Inputs",
           *[f"- **{k}:** {v}" for k, v in report["inputs"].items()], "",
           "## Variation capture", f"Mean text similarity: {report['diversity_analysis']['mean_text_similarity']}",
           f"Variation tags covered: {', '.join(report['diversity_analysis']['variation_coverage'])}",
           "", "Similarity is lexical and is not a semantic originality score."]
    for c in report["candidates"]:
        out += ["", f"## {c['title']}", f"**Logline:** {c['logline']}",
                f"**Utility reward:** {c['reward_score']}/10", "",
                "| Utility component | Score |", "|---|---:|"]
        out.extend(f"| {k} | {v}/10 |" for k, v in c["utility_components"].items())
        out += ["", "### Causal summary", c["causal_summary"], "", "### Scene draft", c["script_draft"],
                "", "### Reward caveat", c["reward_caveat"]]
    return "\n".join(out) + "\n"

def alternate_plots_markdown(report: dict[str, Any]) -> str:
    """Export each generated plot branch as a standalone, portable Markdown file."""
    out = [
        "# CANCE — Alternate Plot Branches",
        "",
        f"**Working title:** {report['inputs'].get('title', 'Untitled Film')}",
        f"**Generated (UTC):** {report['generated_at_utc']}",
        f"**Number of alternatives:** {len(report['candidates'])}",
        "",
        "> These are generated screenplay scaffolds. Reward values are heuristic proxies, not validated audience ratings.",
    ]
    for c in report["candidates"]:
        out.extend([
            "",
            "---",
            "",
            f"## Alternative {c.get('rank', c['id'])}: {c['title']}",
            "",
            f"**Genre / tone:** {c['genre']} / {c['tone']}",
            f"**Variation operator:** {c['variation']}",
            f"**Utility reward:** {c['reward_score']}/10",
            f"**Logline:** {c['logline']}",
            "",
            "### Causal path",
            c["causal_summary"],
            "",
            "### Scene-by-scene plot",
            c["script_draft"],
            "",
            "### Variation tags",
            ", ".join(c["variation_tags"]),
        ])
    return "\\n".join(out) + "\\n"

st.set_page_config(page_title="CANCE Movie Generator", page_icon="🎬", layout="wide")
st.title("CANCE · Causal Movie Generator")
st.caption("Generate multiple film trajectories, score them with a transparent utility function, and measure variation.")
st.markdown("Build an original film concept from a premise. CANCE creates alternative causal paths, scene-beat drafts, a configurable reward score, and a variation report. It generates screenplay scaffolds rather than finished production-ready scripts.")

with st.sidebar:
    st.header("Film concept")
    title = st.text_input("Working title", "The Last Signal")
    genre = st.selectbox("Genre", GENRES)
    tone = st.selectbox("Tone", TONES, index=0)
    premise = st.text_area("Premise / initial situation", height=110, placeholder="What is happening, and why now?")
    protagonist = st.text_input("Protagonist", "A systems engineer")
    goal = st.text_input("Primary goal", "discover why a city-wide warning system is sending false alerts")
    stakes = st.text_input("Stakes", "the city ignoring the one warning that matters")
    constraints = st.text_area("Story constraints / invariants", "Keep technology plausible, preserve the protagonist's core motivation, and make each turning point follow from earlier scenes.", height=90)
    scene_count = st.slider("Scene beats per candidate", 4, 8, 8)
    candidate_count = st.slider("Alternative film trajectories", 3, 10, 5)
    st.header("Reward utility weights")
    st.caption("Increase a weight to prioritize that criterion. Scores are heuristic proxies, not learned reward values.")
    weights = {
        "Causal coherence": st.slider("Causal coherence", 0.0, 5.0, 3.0, 0.5),
        "Character / goal continuity": st.slider("Character continuity", 0.0, 5.0, 2.5, 0.5),
        "Variation capture": st.slider("Variation / diversity", 0.0, 5.0, 2.5, 0.5),
        "Premise specificity": st.slider("Premise specificity", 0.0, 5.0, 2.0, 0.5),
        "Payoff structure": st.slider("Payoff / ending", 0.0, 5.0, 2.0, 0.5),
        "Constraint adherence (proxy)": st.slider("Constraint adherence", 0.0, 5.0, 2.0, 0.5),
    }
    generate = st.button("Generate film variations", type="primary", use_container_width=True)

if "cance_movie_report" not in st.session_state:
    st.session_state.cance_movie_report = None

if generate:
    if len(premise.strip()) < 15:
        st.error("Add a premise of at least 15 characters to generate useful branches.")
    elif not protagonist.strip() or not goal.strip() or not stakes.strip():
        st.error("Fill in the protagonist, goal, and stakes.")
    else:
        inputs = {"title": title, "genre": genre, "tone": tone, "premise": premise,
                  "protagonist": protagonist, "goal": goal, "stakes": stakes,
                  "constraints": constraints, "scene_count": scene_count, "candidate_count": candidate_count,
                  "utility_weights": weights}
        candidates = build_candidates(title, premise, protagonist, goal, stakes, constraints, genre, tone, scene_count, candidate_count)
        candidates = [score_candidate(c, candidates, weights, constraints) for c in candidates]
        candidates.sort(key=lambda c: c["reward_score"], reverse=True)
        for rank, candidate in enumerate(candidates, 1):
            candidate["rank"] = rank
        diversity = score_diversity(candidates)
        st.session_state.cance_movie_report = make_report(inputs, candidates, diversity)

report = st.session_state.cance_movie_report
if report is None:
    st.subheader("Movie-generation pipeline")
    st.code("Premise → causal variation operators → alternative beat sheets → reward utility → variation capture → ranked candidates → export", language="text")
    st.markdown("**Example:** Keep a protagonist and goal fixed while varying what they learn, who cooperates, what resource fails, and what moral cost the climax demands.")
else:
    candidates = report["candidates"]
    diversity = report["diversity_analysis"]
    a, b, c, d = st.columns(4)
    a.metric("Film trajectories", len(candidates))
    b.metric("Scene beats", report["inputs"]["scene_count"])
    c.metric("Variation tags captured", diversity["variation_coverage_count"])
    d.metric("Mean text similarity", diversity["mean_text_similarity"])
    st.warning("Utility scores and lexical variation metrics are prototype heuristics. Review candidates for semantic novelty, causal plausibility, and actual adherence to your constraints.")
    st.subheader("Ranked film concepts")
    for candidate in candidates:
        with st.expander(f"#{candidate['rank']} · {candidate['title']} · Utility {candidate['reward_score']}/10", expanded=(candidate["rank"] == 1)):
            st.markdown(f"**Genre / tone:** {candidate['genre']} / {candidate['tone']}")
            st.markdown(f"**Logline:** {candidate['logline']}")
            st.markdown("**Causal path**")
            st.write(candidate["causal_summary"])
            st.markdown("**Reward utility components**")
            st.dataframe([{"Criterion": k, "Heuristic score (0–10)": v, "Weight": report["inputs"]["utility_weights"][k]} for k, v in candidate["utility_components"].items()], hide_index=True, use_container_width=True)
            st.markdown("**Scene-beat screenplay draft**")
            st.text(candidate["script_draft"])
            st.caption(candidate["reward_caveat"])
    st.subheader("Variation capture")
    st.write("Tags represented across candidates: " + ", ".join(diversity["variation_coverage"]))
    st.write(diversity["interpretation"])
    if diversity["pairwise"]:
        st.dataframe([{"Candidate A": p["a"], "Candidate B": p["b"], "Text similarity": p["similarity"], "Variation distance": p["variation_distance"]} for p in diversity["pairwise"]], hide_index=True, use_container_width=True)
    st.subheader("Export")
    left, middle, right = st.columns(3)
    left.download_button("Download full Markdown report", markdown_report(report), file_name="cance_movie_generator_report.md", mime="text/markdown", use_container_width=True)
    middle.download_button("Save alternate plots (.md)", alternate_plots_markdown(report), file_name="cance_alternate_plots.md", mime="text/markdown", use_container_width=True)
    right.download_button("Download JSON candidates + reward scores", json.dumps(report, ensure_ascii=False, indent=2), file_name="cance_movie_generator_report.json", mime="application/json", use_container_width=True)
    st.caption("CANCE Movie Generator v" + APP_VERSION + " · The current version generates structured scene-beat drafts, not finished film or video.")

st.divider()
st.caption("Reward-based selection is explicit and inspectable. For a production-grade generator, replace heuristic quality proxies with human preference feedback and a validated reward model.")
