import json
import pandas as pd
import streamlit as st
from sai_core import QueryEvent, IndexStat, classify_workload, index_recommendations, validate_guardrails

st.set_page_config(page_title="SAI Indexing", layout="wide")
st.title("Structural Adaptive Indexing")
st.caption("Monitoring-first, recommendation-only prototype")

sample_queries = pd.DataFrame([
    {"query_id":"q1", "workload":"OLTP", "latency_ms":25, "calls":1200, "indexed":True},
    {"query_id":"q2", "workload":"OLAP", "latency_ms":220, "calls":80, "indexed":False},
    {"query_id":"q3", "workload":"HYBRID", "latency_ms":140, "calls":300, "indexed":False},
])
sample_indexes = pd.DataFrame([
    {"name":"idx_customer", "scans":1800, "writes":500, "size_mb":240},
    {"name":"idx_legacy", "scans":0, "writes":900, "size_mb":700},
])
queries = st.data_editor(sample_queries, num_rows="dynamic", use_container_width=True)
indexes = st.data_editor(sample_indexes, num_rows="dynamic", use_container_width=True)
load = st.slider("System load (%)", 0, 100, 45)
changes = st.number_input("Changes in last hour", min_value=0, value=0)

if st.button("Analyze workload"):
    events = [QueryEvent(**r) for r in queries.to_dict("records")]
    stats = [IndexStat(**r) for r in indexes.to_dict("records")]
    workload = classify_workload(events)
    recs = index_recommendations(events, stats)
    allowed, reason = validate_guardrails(recs, changes, load, {"max_changes_per_hour":3,"high_load_threshold_percent":80})
    st.metric("Workload classification", workload)
    st.info(reason)
    st.dataframe(pd.DataFrame(recs), use_container_width=True)
    st.download_button("Download audit report", json.dumps({"workload":workload,"recommendations":recs,"guardrails":reason}, indent=2), "sai_report.json", "application/json")
