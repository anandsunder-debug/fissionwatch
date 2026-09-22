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

## Layout
- `app.py` — Streamlit dashboard
- `sai_core.py` — analysis and decision logic
- `config.yaml` — conservative defaults
- `tests/test_sai_core.py` — unit tests
