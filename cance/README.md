# CANCE — Counterfactual Narrative Engine

A small Streamlit prototype for causal what-if analysis of narrative decisions. The initial case study is *Zubeidaa* (2001), with five relationship-mediated information interventions.

## Features

- Five counterfactual branches, each with intervention, causal chain, character response, alternative ending, thematic implications, assumptions, and qualitative uncertainty.
- Explicit separation between broad established story facts and invented counterfactual events.
- Character-preservation checklist.
- Markdown and JSON report export.
- No fabricated empirical probabilities.

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

1. Review or edit the intervention text in the sidebar.
2. Select one or more of the five branches.
3. Review the character-preservation checklist and add analyst notes.
4. Expand a branch to inspect its causal chain, assumptions, ending, and uncertainty.
5. Download a Markdown report for reading or a JSON report for downstream processing.

## Causal interpretation

The app uses the conceptual transition:

`X[t+1] = F(X[t], A[t], W[t])`

with a hypothetical intervention `do(I[t] = i)`. Here `X` is narrative state, `A` is the character's action, and `W` represents external circumstances. A belief change does not guarantee a decision change, and a decision change does not guarantee a different outcome.

## Evidence and limitations

- The app is a qualitative analysis prototype, not a predictive model trained on annotated scripts.
- The baseline facts are broad narrative elements, not a scene-by-scene verified dataset.
- Each disclosure and alternative ending is explicitly hypothetical.
- Uncertainty labels are qualitative, not calibrated probabilities.
- The final-flight branch does not assume a specific preventable warning, mechanical defect, or definitive causal explanation.

For research-grade use, annotate scenes, character knowledge states, decision points, causal dependencies, and downstream consequences. Evaluate branches for character consistency, causal traceability, and minimal-change consistency.

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
