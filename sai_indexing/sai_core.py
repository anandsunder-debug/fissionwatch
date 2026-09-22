from dataclasses import dataclass
from typing import Iterable
import math

@dataclass(frozen=True)
class QueryEvent:
    query_id: str
    workload: str
    latency_ms: float
    calls: int
    indexed: bool

@dataclass(frozen=True)
class IndexStat:
    name: str
    scans: int
    writes: int
    size_mb: float


def classify_workload(events: Iterable[QueryEvent]) -> str:
    events = list(events)
    if not events:
        return "UNKNOWN"
    analytical = sum(e.calls for e in events if e.latency_ms >= 100)
    total = sum(e.calls for e in events) or 1
    ratio = analytical / total
    if ratio >= 0.60:
        return "OLAP"
    if ratio <= 0.25:
        return "OLTP"
    return "HYBRID"


def index_recommendations(events, indexes, min_roi_percent=10):
    events = list(events)
    indexes = list(indexes)
    recommendations = []
    for idx in indexes:
        maintenance_cost = idx.writes * max(idx.size_mb, 1) * 0.01
        usage_value = idx.scans * 0.5
        if idx.scans == 0 and idx.writes > 0:
            recommendations.append({"action": "REVIEW_UNUSED", "index": idx.name,
                                    "estimated_roi_percent": round(maintenance_cost, 2),
                                    "reason": "No observed scans; validate before removal."})
        elif usage_value > maintenance_cost and usage_value >= min_roi_percent:
            recommendations.append({"action": "RETAIN", "index": idx.name,
                                    "estimated_roi_percent": round(usage_value - maintenance_cost, 2),
                                    "reason": "Observed usage outweighs estimated maintenance cost."})
    for event in events:
        if not event.indexed and event.latency_ms >= 100:
            score = min(95.0, math.log1p(event.calls) * event.latency_ms / 10)
            recommendations.append({"action": "REVIEW_ADD_INDEX", "query_id": event.query_id,
                                    "estimated_roi_percent": round(score, 2),
                                    "reason": "High-latency query without observed index support."})
    return sorted(recommendations, key=lambda x: x["estimated_roi_percent"], reverse=True)


def validate_guardrails(recommendations, changes_last_hour, system_load_percent, config):
    if system_load_percent >= config.get("high_load_threshold_percent", 80):
        return False, "System load is above the configured threshold."
    if changes_last_hour >= config.get("max_changes_per_hour", 3):
        return False, "Hourly change limit reached."
    if not recommendations:
        return False, "No recommendations available."
    return True, "Recommendations may be reviewed; execution remains disabled."
