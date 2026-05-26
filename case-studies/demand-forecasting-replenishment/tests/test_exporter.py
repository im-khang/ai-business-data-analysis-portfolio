import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

CASE_ROOT = Path(__file__).resolve().parents[1]
EXPORTER = CASE_ROOT / "dashboard" / "export_pages_data.py"
sys.path.insert(0, str(CASE_ROOT / "dashboard"))

import export_pages_data as exporter


def _sample_metrics() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "store_nbr": 44,
                "item_nbr": 1011,
                "family": "GROCERY I",
                "actual_units": 980.0,
                "avg_daily_units": 35.0,
                "wape_pct": 22.5,
                "mae_units": 6.4,
                "bias_pct": -12.0,
                "forecast_score": 65.5,
                "fva_pct": 18.0,
                "demand_cv": 0.45,
                "safety_stock_units": 32.0,
                "reorder_point_units": 277.0,
                "lead_time_days": 7,
                "service_level_assumption": "90% (z=1.28)",
                "abc_class": "A",
                "xyz_class": "X",
                "reason_codes": "high_volume,under_forecast_bias",
                "recommended_action": "Review safety-stock and lead-time assumptions before replenishment decision.",
                "exception_score": 92.5,
            },
            {
                "store_nbr": 12,
                "item_nbr": 2055,
                "family": "BEVERAGES",
                "actual_units": 410.0,
                "avg_daily_units": 14.6,
                "wape_pct": 38.0,
                "mae_units": 5.1,
                "bias_pct": 8.0,
                "forecast_score": 54.0,
                "fva_pct": 5.0,
                "demand_cv": 1.6,
                "safety_stock_units": 18.0,
                "reorder_point_units": 121.2,
                "lead_time_days": 7,
                "service_level_assumption": "90% (z=1.28)",
                "abc_class": "B",
                "xyz_class": "Z",
                "reason_codes": "high_error,volatile_demand",
                "recommended_action": "Monitor intermittent demand and avoid automatic reorder escalation.",
                "exception_score": 71.0,
            },
        ]
    )


@pytest.fixture
def tmp_layout(tmp_path):
    processed = tmp_path / "processed"
    public = tmp_path / "public"
    processed.mkdir()
    public.mkdir()
    return processed, public


def test_missing_processed_csv_exits_zero_and_no_overwrite(tmp_layout):
    processed, public = tmp_layout
    existing = public / "kpis.json"
    existing.write_text(json.dumps({"prior": True}))
    code = exporter.run(processed_dir=processed, public_dir=public, check=False)
    assert code == 0
    assert json.loads(existing.read_text()) == {"prior": True}


def test_export_writes_aggregate_jsons_within_budget(tmp_layout):
    processed, public = tmp_layout
    _sample_metrics().to_csv(processed / "planner_metrics.csv", index=False)
    code = exporter.run(processed_dir=processed, public_dir=public, check=False)
    assert code == 0
    expected = {
        "kpis.json",
        "forecast_accuracy.json",
        "planner_queue.json",
        "segments.json",
        "assumptions.json",
        "build_metadata.json",
    }
    assert {p.name for p in public.iterdir()} >= expected
    metadata = json.loads((public / "build_metadata.json").read_text())
    assert metadata["json_total_bytes"] <= 2 * 1024 * 1024
    assert metadata["json_max_file_bytes"] <= 500 * 1024
    assert metadata["row_counts"]["planner_queue"] == 2
    queue = json.loads((public / "planner_queue.json").read_text())
    assert queue["rows"][0]["reason_codes"] == ["high_volume", "under_forecast_bias"]
    assert "recommended_action" in queue["rows"][0]


def test_oversize_file_returns_non_zero(tmp_layout, monkeypatch):
    processed, public = tmp_layout
    _sample_metrics().to_csv(processed / "planner_metrics.csv", index=False)
    monkeypatch.setattr(exporter, "MAX_FILE_BYTES", 32)
    code = exporter.run(processed_dir=processed, public_dir=public, check=False)
    assert code != 0


def test_check_mode_validates_without_rewriting(tmp_layout):
    processed, public = tmp_layout
    _sample_metrics().to_csv(processed / "planner_metrics.csv", index=False)
    assert exporter.run(processed_dir=processed, public_dir=public, check=False) == 0
    snapshot = (public / "build_metadata.json").read_text()
    assert exporter.run(processed_dir=processed, public_dir=public, check=True) == 0
    assert (public / "build_metadata.json").read_text() == snapshot


def test_check_mode_fails_when_required_json_missing(tmp_layout):
    _processed, public = tmp_layout
    assert exporter.run(processed_dir=_processed, public_dir=public, check=True) != 0


def test_exporter_rejects_missing_required_columns(tmp_layout):
    processed, public = tmp_layout
    pd.DataFrame([{"store_nbr": 1}]).to_csv(processed / "planner_metrics.csv", index=False)
    assert exporter.run(processed_dir=processed, public_dir=public, check=False) != 0


def test_planner_queue_truncates_to_25_rows(tmp_layout):
    processed, public = tmp_layout
    rows = pd.concat([_sample_metrics()] * 20, ignore_index=True)
    rows["exception_score"] = range(len(rows))
    rows.to_csv(processed / "planner_metrics.csv", index=False)
    assert exporter.run(processed_dir=processed, public_dir=public, check=False) == 0
    queue = json.loads((public / "planner_queue.json").read_text())
    assert len(queue["rows"]) == 25


def test_cli_entrypoint_runs(tmp_layout):
    processed, public = tmp_layout
    _sample_metrics().to_csv(processed / "planner_metrics.csv", index=False)
    completed = subprocess.run(
        [sys.executable, str(EXPORTER), "--processed-dir", str(processed), "--public-dir", str(public)],
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
