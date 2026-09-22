from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import xml.etree.ElementTree as ET


def parse_junit(path: Path) -> dict[str, float | int]:
    root = ET.parse(path).getroot()
    if root.tag == "testsuites":
        tests = int(root.attrib.get("tests", 0))
        failures = int(root.attrib.get("failures", 0))
        errors = int(root.attrib.get("errors", 0))
        skipped = int(root.attrib.get("skipped", 0))
        time_s = float(root.attrib.get("time", 0.0))
    elif root.tag == "testsuite":
        tests = int(root.attrib.get("tests", 0))
        failures = int(root.attrib.get("failures", 0))
        errors = int(root.attrib.get("errors", 0))
        skipped = int(root.attrib.get("skipped", 0))
        time_s = float(root.attrib.get("time", 0.0))
    else:
        raise ValueError(f"Unsupported JUnit root tag: {root.tag}")
    passed = max(tests - failures - errors - skipped, 0)
    return {
        "tests": tests,
        "failures": failures,
        "errors": errors,
        "skipped": skipped,
        "passed": passed,
        "time_s": round(time_s, 3),
    }


def load_metrics(path: Path) -> dict[str, str]:
    metrics = {}
    if path.exists():
        try:
            payload = json.loads(path.read_text())
        except json.JSONDecodeError:
            payload = {}
        metrics["learning_rate"] = str(payload.get("learning_rate", "N/A"))
        metrics["train_error"] = str(payload.get("train_error", "N/A"))
        metrics["validation_error"] = str(payload.get("validation_error", "N/A"))
        metrics["error_overview"] = str(payload.get("error_overview", "N/A"))
        return metrics

    metrics["learning_rate"] = os.getenv("SAI_LEARNING_RATE", "N/A")
    metrics["train_error"] = os.getenv("SAI_TRAIN_ERROR", "N/A")
    metrics["validation_error"] = os.getenv("SAI_VALIDATION_ERROR", "N/A")
    metrics["error_overview"] = os.getenv("SAI_ERROR_OVERVIEW", "N/A")
    return metrics


def render_html(summary: dict[str, float | int], metrics: dict[str, str]) -> str:
    status = "PASS" if summary["failures"] == 0 and summary["errors"] == 0 else "FAIL"
    status_color = "#0f766e" if status == "PASS" else "#b91c1c"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>SAI Core Test Report</title>
  <style>
    :root {{
      --bg: #f6f8fb;
      --card: #ffffff;
      --text: #1f2937;
      --muted: #6b7280;
      --accent: #0f766e;
      --danger: #b91c1c;
      --border: #e5e7eb;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif;
      background: linear-gradient(180deg, #eef3ff 0%, var(--bg) 35%, #f9fafb 100%);
      color: var(--text);
    }}
    .wrap {{
      max-width: 980px;
      margin: 32px auto;
      padding: 0 16px;
    }}
    .card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 16px;
      box-shadow: 0 8px 24px rgba(17, 24, 39, 0.05);
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 1.7rem;
    }}
    .status {{
      display: inline-block;
      padding: 6px 12px;
      border-radius: 999px;
      color: white;
      font-weight: 600;
      background: {status_color};
    }}
    .grid {{
      display: grid;
      gap: 10px;
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    }}
    .kpi {{
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px;
      background: #fbfdff;
    }}
    .label {{
      color: var(--muted);
      font-size: 0.84rem;
      margin-bottom: 4px;
    }}
    .value {{
      font-size: 1.22rem;
      font-weight: 700;
    }}
    a {{
      color: var(--accent);
      text-decoration: none;
      font-weight: 600;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="card">
      <h1>SAI Core Test Results</h1>
      <div class="status">{status}</div>
      <p>Quick visual summary of test execution with optional learning/error metrics.</p>
    </section>

    <section class="card">
      <h2>Test Summary</h2>
      <div class="grid">
        <div class="kpi"><div class="label">Total</div><div class="value">{summary["tests"]}</div></div>
        <div class="kpi"><div class="label">Passed</div><div class="value">{summary["passed"]}</div></div>
        <div class="kpi"><div class="label">Failed</div><div class="value">{summary["failures"]}</div></div>
        <div class="kpi"><div class="label">Errors</div><div class="value">{summary["errors"]}</div></div>
        <div class="kpi"><div class="label">Skipped</div><div class="value">{summary["skipped"]}</div></div>
        <div class="kpi"><div class="label">Duration (s)</div><div class="value">{summary["time_s"]}</div></div>
      </div>
    </section>

    <section class="card">
      <h2>Learning And Error Overview</h2>
      <div class="grid">
        <div class="kpi"><div class="label">Learning Rate</div><div class="value">{metrics["learning_rate"]}</div></div>
        <div class="kpi"><div class="label">Train Error</div><div class="value">{metrics["train_error"]}</div></div>
        <div class="kpi"><div class="label">Validation Error</div><div class="value">{metrics["validation_error"]}</div></div>
      </div>
      <p><strong>Error Overview:</strong> {metrics["error_overview"]}</p>
      <p>If `test-results/metrics.json` exists, values are sourced from that file. Otherwise, the report reads
      `SAI_LEARNING_RATE`, `SAI_TRAIN_ERROR`, `SAI_VALIDATION_ERROR`, and `SAI_ERROR_OVERVIEW` from environment variables.</p>
    </section>

    <section class="card">
      <a href="./pytest-report.html">Open full pytest HTML report</a>
    </section>
  </div>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--junit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metrics", type=Path, required=True)
    args = parser.parse_args()

    summary = parse_junit(args.junit)
    metrics = load_metrics(args.metrics)
    args.output.write_text(render_html(summary, metrics))


if __name__ == "__main__":
    main()
