from sai_core import QueryEvent, IndexStat, classify_workload, index_recommendations, validate_guardrails


def test_workload_classification():
    events = [QueryEvent("q1", "OLTP", 20, 100, True), QueryEvent("q2", "OLAP", 200, 10, False)]
    assert classify_workload(events) in {"OLTP", "HYBRID", "OLAP"}


def test_unused_index_review():
    recs = index_recommendations([], [IndexStat("old", 0, 100, 100)])
    assert recs[0]["action"] == "REVIEW_UNUSED"


def test_guardrail_high_load():
    ok, reason = validate_guardrails([{"action":"REVIEW"}], 0, 90, {})
    assert not ok
    assert "load" in reason.lower()
