from fissionwatch.telemetry.scrape import EdgeTelemetry, TelemetryMapping


def test_error_ratio_is_safe():
    assert EdgeTelemetry("a", "b", errors_per_second=2, calls_per_second=4).error_ratio == 0.5
    assert EdgeTelemetry("a", "b").error_ratio == 0.0


def test_mapping_is_configurable():
    m = TelemetryMapping(source_label="caller", target_label="callee", query_window="1m")
    assert m.source_label == "caller"
    assert m.query_window == "1m"
