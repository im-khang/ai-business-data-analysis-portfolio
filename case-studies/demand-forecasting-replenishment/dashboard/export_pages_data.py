#!/usr/bin/env python3
"""Export aggregate Favorita planner metrics to static GitHub Pages JSON."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

CASE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROCESSED_DIR = CASE_ROOT / "data" / "processed"
DEFAULT_PUBLIC_DIR = Path(__file__).resolve().parents[3] / "docs" / "demand-forecasting-replenishment" / "assets" / "data"
MAX_FILE_BYTES = 500 * 1024
MAX_TOTAL_BYTES = 2 * 1024 * 1024
PROCESSED_FILE = "planner_metrics.csv"
REQUIRED_JSON = {"kpis.json", "forecast_accuracy.json", "planner_queue.json", "segments.json", "assumptions.json", "build_metadata.json"}
REQUIRED_COLUMNS = {
    "store_nbr", "item_nbr", "family", "actual_units", "avg_daily_units", "wape_pct", "mae_units", "bias_pct",
    "forecast_score", "fva_pct", "demand_cv", "safety_stock_units", "reorder_point_units", "lead_time_days",
    "service_level_assumption", "abc_class", "xyz_class", "reason_codes", "recommended_action", "exception_score",
}


def _records(df: pd.DataFrame) -> list[dict[str, Any]]:
    return df.where(pd.notna(df), None).to_dict(orient="records")


def _split_reasons(value: Any) -> list[str]:
    if value is None or pd.isna(value):
        return []
    return [part.strip() for part in str(value).split(",") if part.strip()]


def _validate_processed_schema(df: pd.DataFrame) -> list[str]:
    missing = sorted(REQUIRED_COLUMNS - set(df.columns))
    return [f"missing columns: {missing}"] if missing else []


def _payloads(df: pd.DataFrame) -> dict[str, Any]:
    errors = _validate_processed_schema(df)
    if errors:
        raise ValueError("; ".join(errors))
    queue = df.sort_values("exception_score", ascending=False).head(25).copy()
    queue["reason_codes"] = queue["reason_codes"].apply(_split_reasons)
    kpis = {
        "dataset": "Corporación Favorita Grocery Sales Forecasting",
        "grain": "store_nbr + item_nbr + family over holdout window",
        "items_in_queue": int(len(df)),
        "avg_wape_pct": round(float(df["wape_pct"].dropna().mean()), 2) if df["wape_pct"].notna().any() else None,
        "avg_bias_pct": round(float(df["bias_pct"].dropna().mean()), 2) if df["bias_pct"].notna().any() else None,
        "avg_forecast_score": round(float(df["forecast_score"].dropna().mean()), 2) if df["forecast_score"].notna().any() else None,
        "top_exception_score": round(float(df["exception_score"].max()), 2) if not df.empty else None,
        "planning_caveat": "Planning assumption — not production-order recommendation.",
    }
    accuracy_cols = ["family", "abc_class", "xyz_class", "wape_pct", "mae_units", "bias_pct", "forecast_score", "fva_pct"]
    segment = (df.groupby(["abc_class", "xyz_class"], as_index=False)
               .agg(items=("item_nbr", "count"), avg_wape_pct=("wape_pct", "mean"), avg_exception_score=("exception_score", "mean"))
               .round(2))
    return {
        "kpis.json": kpis,
        "forecast_accuracy.json": {"rows": _records(df[accuracy_cols].sort_values("wape_pct", ascending=False).head(50))},
        "planner_queue.json": {"rows": _records(queue)},
        "segments.json": {"rows": _records(segment)},
        "assumptions.json": {
            "lead_time_days": 7,
            "service_level_assumption": "90% (z=1.28)",
            "review_policy": "Use queue as review candidates, not automatic order instructions.",
            "inventory_limit": "Public Favorita data does not include true stock on hand, purchase orders, or supplier lead-time history.",
            "zero_demand_handling": "WAPE returns null when actual demand denominator is zero.",
        },
    }


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str) + "\n")


def _validate_json_dir(public_dir: Path) -> dict[str, Any]:
    files = sorted(public_dir.glob("*.json"))
    names = {p.name for p in files}
    missing = sorted(REQUIRED_JSON - names)
    parse_errors = []
    for p in files:
        try:
            json.loads(p.read_text())
        except json.JSONDecodeError as exc:
            parse_errors.append(f"{p.name}: {exc}")
    sizes = {p.name: p.stat().st_size for p in files}
    total = sum(sizes.values())
    max_file = max(sizes.values(), default=0)
    violations = [name for name, size in sizes.items() if size > MAX_FILE_BYTES]
    if total > MAX_TOTAL_BYTES:
        violations.append("TOTAL_JSON_BYTES")
    return {"sizes": sizes, "total": total, "max_file": max_file, "violations": violations, "missing": missing, "parse_errors": parse_errors}


def _write_payloads_with_metadata(target_dir: Path, payloads: dict[str, Any]) -> dict[str, Any]:
    target_dir.mkdir(parents=True, exist_ok=True)
    for old in target_dir.glob("*.json"):
        old.unlink()
    for name, payload in payloads.items():
        _write_json(target_dir / name, payload)
    metadata = {
        "dataset": "Corporación Favorita Grocery Sales Forecasting",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "row_counts": {
            "planner_metrics": int(payloads["kpis.json"]["items_in_queue"]),
            "planner_queue": int(len(payloads["planner_queue.json"]["rows"])),
            "segments": int(len(payloads["segments.json"]["rows"])),
        },
        "json_total_bytes": 0,
        "json_max_file_bytes": 0,
        "json_file_bytes": {},
        "caveat": "Aggregate JSON only. Raw data remains local and ignored by git.",
    }
    _write_json(target_dir / "build_metadata.json", metadata)
    validation = _validate_json_dir(target_dir)
    metadata["json_total_bytes"] = validation["total"]
    metadata["json_max_file_bytes"] = validation["max_file"]
    metadata["json_file_bytes"] = validation["sizes"]
    _write_json(target_dir / "build_metadata.json", metadata)
    validation = _validate_json_dir(target_dir)
    metadata["json_total_bytes"] = validation["total"]
    metadata["json_max_file_bytes"] = validation["max_file"]
    metadata["json_file_bytes"] = validation["sizes"]
    _write_json(target_dir / "build_metadata.json", metadata)
    return _validate_json_dir(target_dir)


def run(processed_dir: Path = DEFAULT_PROCESSED_DIR, public_dir: Path = DEFAULT_PUBLIC_DIR, check: bool = False) -> int:
    processed_dir = Path(processed_dir)
    public_dir = Path(public_dir)
    processed_file = processed_dir / PROCESSED_FILE
    if check:
        validation = _validate_json_dir(public_dir)
        problems = validation["missing"] + validation["parse_errors"] + validation["violations"]
        if problems:
            print(f"JSON check failed: {problems}")
            return 2
        print("Existing JSON schema and size check passed.")
        return 0
    if not processed_file.exists():
        print(f"Processed metrics missing: {processed_file}")
        print("Run notebooks/01_run_pipeline.py after placing raw Favorita data locally.")
        return 0
    try:
        df = pd.read_csv(processed_file)
        payloads = _payloads(df)
        with tempfile.TemporaryDirectory(prefix="favorita-export-") as tmp:
            tmp_dir = Path(tmp)
            validation = _write_payloads_with_metadata(tmp_dir, payloads)
            problems = validation["missing"] + validation["parse_errors"] + validation["violations"]
            if problems:
                print(f"JSON export failed before publish: {problems}")
                return 2
            public_dir.mkdir(parents=True, exist_ok=True)
            for old in public_dir.glob("*.json"):
                old.unlink()
            for src in tmp_dir.glob("*.json"):
                shutil.copy2(src, public_dir / src.name)
    except Exception as exc:
        print(f"Export failed: {exc}")
        return 2
    print(f"Exported aggregate JSON to {public_dir}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    parser.add_argument("--public-dir", type=Path, default=DEFAULT_PUBLIC_DIR)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return run(processed_dir=args.processed_dir, public_dir=args.public_dir, check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
