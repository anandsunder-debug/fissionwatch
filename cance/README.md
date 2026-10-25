# CANCE — Causal Analysis and Counterfactual Narrative Engine

CANCE is a generic Streamlit prototype for exploring how a change to any user-supplied plot, screenplay, novel, game narrative, or scenario can lead to multiple alternative outcomes. It creates structured causal chains so a reader can inspect the link between a counterfactual intervention, a decision, and downstream consequences.

## Features

- Paste any plot or synopsis; identify a consequential decision and a what-if intervention.
- Generate 3–10 alternative outcome branches using distinct causal lenses.
- Inspect a seven-step chain: baseline, intervention, mechanism, decision response, immediate consequence, downstream propagation, and outcome.
- Specify character-preservation constraints and world / chronology constraints.
- View each branch's assumptions, evidence basis, hypothesis status, and consistency checks.
- Export the full analysis as Markdown or JSON.
- No invented numeric probabilities.

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

Open the local URL printed by Streamlit (typically http://localhost:8501).

## How to use

1. Paste a plot, synopsis, scene, quest, or scenario into **Plot / synopsis**.
2. Enter the key decision or turning point.
3. State the counterfactual change (for example, a witness reveals evidence earlier).
4. Specify character traits and world constraints that must remain consistent.
5. Choose the tone and number of outcomes, then select **Generate counterfactual outcomes**.
6. Expand each outcome and audit every causal step and its stated basis.
7. Download the Markdown report for review or JSON for downstream processing.

## Causal model

Each branch follows the conceptual chain:

`Baseline → Intervention → Mechanism → Decision response → Immediate consequence → Feedback → Alternative outcome`

The purpose is traceability, not certainty. A changed input may not change a decision; a changed decision may not change the final outcome; other characters and external events can amplify or reverse an effect.

## Important limitations

- This version is a **structured, rule-based scaffold**, not an LLM-powered story-understanding system. It uses the supplied plot and user constraints as text, and generates branch drafts from causal templates.
- It does not independently verify plot facts, understand every implied dependency, or retrieve source texts.
- The generated narratives are hypotheses to revise, not canonical facts, forecasts, or claims of what an author intended.
- Uncertainty is qualitative; the app does not calculate calibrated likelihoods.
- For higher-quality analysis, make the decision point and intervention specific, add explicit character/world constraints, and manually review whether each causal edge is justified.
- A future LLM integration could enrich plot parsing, extract characters and events, build a scene-level causal graph, and critique unsupported links. That integration is not included in this version.

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
