# Structural Adaptive Indexing (SAI)

A monitoring-first prototype for workload-aware database index recommendations.

## Scope
- Query telemetry ingestion with sampling
- Workload classification: OLTP, OLAP, HYBRID
- Index usage and bottleneck analysis
- Cost/benefit scoring and guarded recommendations
- Audit-ready JSON output

> **Safety:** This prototype is recommendation-only. It does not execute DDL, drop indexes, rebuild indexes, or change production schemas.

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## CI Test Reports
- The `SAI tests` workflow can be triggered manually (`workflow_dispatch`) and on `push`/`pull_request` for `sai_indexing/**`.
- CI publishes `sai-test-results` artifact containing:
  - `pytest-report.html` (full pytest HTML report)
  - `junit.xml` (machine-readable test results)
  - `index.html` (visual summary with pass/fail and metrics)
- Optional learning/error metrics can be captured in `test-results/metrics.json` with keys:
  - `learning_rate`, `train_error`, `validation_error`, `error_overview`
  - If the file is absent, CI falls back to env vars: `SAI_LEARNING_RATE`, `SAI_TRAIN_ERROR`, `SAI_VALIDATION_ERROR`, `SAI_ERROR_OVERVIEW`.

## Layout
- `app.py` — Streamlit dashboard
- `sai_core.py` — analysis and decision logic
- `config.yaml` — conservative defaults
- `tests/test_sai_core.py` — unit tests
