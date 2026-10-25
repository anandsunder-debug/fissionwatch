# CANCE Movie Generator

CANCE is a Streamlit prototype for creating multiple film-story trajectories from an original premise. It combines causal variation operators, scene-beat screenplay drafts, a configurable reward-based utility function, and variation-capture metrics.

## Features

- Define a working title, genre, tone, premise, protagonist, goal, stakes, and story constraints.
- Generate 3–10 alternative film trajectories with 4–8 scene beats each.
- Explore different causal variation operators: information reveal, ally turns, resource constraints, moral reversals, opponent adaptation, path dependence, cooperation, failure/adaptation, perspective shifts, and sacrifice.
- Score each candidate with a transparent weighted utility function.
- Adjust weights for causal coherence, character continuity, variation, premise specificity, payoff structure, and constraint adherence.
- Capture variation tags and calculate pairwise lexical similarity / variation distance.
- Rank candidates and export Markdown or JSON reports.

## Quick start

Python 3.10+ recommended.

\`\`\`bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

python -m pip install -r requirements.txt
streamlit run app.py
\`\`\`

## Reward utility

For candidate \(c\), the prototype computes:

\`U(c) = sum(w_i * q_i(c)) / sum(w_i)\`

where \(w_i\) is the user's weight for a criterion and \(q_i\) is a transparent 0–10 heuristic proxy. The current criteria are causal coherence, character/goal continuity, variation capture, premise specificity, payoff structure, and constraint adherence.

These are **not** scores from a trained reward model, audience research, or a calibrated quality estimator. They are simple, inspectable heuristics intended to support comparison and experimentation. Zero-weight criteria are excluded from the denominator; if all weights are zero, the score is zero.

## Variation capture

Each candidate is built from different causal operators. The app tracks the variation tags used and computes pairwise Jaccard similarity over word sets, then reports variation distance as one minus similarity.

This is only a lexical proxy. Two semantically identical drafts can look different in vocabulary, and two genuinely different stories can share many words. Use the metric as a diagnostic, not a definitive measure of originality.

## Important limitations

- This generates structured film concepts and scene-beat drafts, not finished screenplay pages, filmed video, or production assets.
- It does not yet use a connected LLM to deeply understand a premise, create dialogue, or verify every causal implication.
- Scene text is templated. Human revision is needed for originality, pacing, character voice, and production feasibility.
- The reward function is heuristic and should not be interpreted as an objective truth about story quality.
- For a stronger version, collect human pairwise preferences, validate the scoring rubric, add semantic embeddings for diversity, preserve a story-state graph, and test each branch against explicit continuity constraints.

## Repository layout

\`\`\`
cance/
  app.py
  requirements.txt
  README.md
  tests/
    test_cance.py
\`\`\`

## License

No license is declared by this prototype. Add a license before redistributing if needed.
