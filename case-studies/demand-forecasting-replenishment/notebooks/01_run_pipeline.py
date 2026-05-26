#!/usr/bin/env python3
"""Favorita demand forecasting proof-slice pipeline.

Builds local processed aggregates only. Public JSON export is handled by
`dashboard/export_pages_data.py` so raw data never enters `docs/`.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = CASE_ROOT / "data" / "raw"
PROCESSED_DIR = CASE_ROOT / "data" / "processed"
sys.path.insert(0, str(CASE_ROOT / "dashboard"))

from lib.metrics import bias_pct, forecast_score, fva, mae, wape

REQUIRED_FILES = ["train.csv", "items.csv", "stores.csv"]
OUTPUT = PROCESSED_DIR / "planner_metrics.csv"


def missing_raw_files() -> list[str]:
    return [name for name in REQUIRED_FILES if not (RAW_DIR / name).exists()]


def print_setup_guidance(missing: list[str]) -> None:
    print("Favorita raw data missing. No public assets written.")
    print("Download Corporación Favorita Grocery Sales Forecasting data from Kaggle:")
    print("https://www.kaggle.com/c/favorita-grocery-sales-forecasting/data")
    print(f"Place missing files in {RAW_DIR}:")
    for name in missing:
        print(f"- {name}")


def _read_csv_required(path: Path, columns: list[str], parse_dates: list[str] | None = None) -> pd.DataFrame:
    try:
        return pd.read_csv(path, usecols=columns, parse_dates=parse_dates)
    except ValueError as exc:
        raise ValueError(f"{path.name} missing required columns {columns}: {exc}") from exc


def load_demand() -> pd.DataFrame:
    usecols = ["date", "store_nbr", "item_nbr", "unit_sales"]
    train = _read_csv_required(RAW_DIR / "train.csv", usecols, parse_dates=["date"])
    items = _read_csv_required(RAW_DIR / "items.csv", ["item_nbr", "family"])
    _read_csv_required(RAW_DIR / "stores.csv", ["store_nbr"])
    if train.empty:
        return pd.DataFrame(columns=["date", "store_nbr", "item_nbr", "family", "actual_units"])
    # Returns are negative in Favorita; this proof slice clips them to zero and documents planning-demand only.
    train["unit_sales"] = train["unit_sales"].clip(lower=0)
    recent_start = train["date"].max() - pd.Timedelta(days=180)
    recent = train.loc[train["date"] >= recent_start].merge(items, on="item_nbr", how="left")
    # Controlled proof slice: enough history for planner signals, not full-dataset modeling.
    top_families = recent.groupby("family")["unit_sales"].sum().nlargest(5).index
    top_stores = recent.groupby("store_nbr")["unit_sales"].sum().nlargest(8).index
    sliced = recent[recent["family"].isin(top_families) & recent["store_nbr"].isin(top_stores)]
    if sliced.empty:
        return pd.DataFrame(columns=["date", "store_nbr", "item_nbr", "family", "actual_units"])
    demand = (
        sliced.groupby(["date", "store_nbr", "item_nbr", "family"], as_index=False)["unit_sales"].sum()
        .rename(columns={"unit_sales": "actual_units"})
        .sort_values(["store_nbr", "item_nbr", "date"])
    )
    dupes = demand.duplicated(["date", "store_nbr", "item_nbr"]).sum()
    if dupes:
        raise ValueError(f"duplicate demand grain rows after aggregation: {dupes}")
    return demand


def add_baselines(demand: pd.DataFrame) -> pd.DataFrame:
    if demand.empty:
        return demand.assign(naive_forecast=pd.Series(dtype=float), moving_avg_forecast=pd.Series(dtype=float))
    frames = []
    for (_store, _item, family), g in demand.groupby(["store_nbr", "item_nbr", "family"]):
        daily = g.set_index("date").sort_index()
        full_index = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
        dense = daily.reindex(full_index)
        dense["date"] = dense.index
        dense["store_nbr"] = _store
        dense["item_nbr"] = _item
        dense["family"] = family
        dense["actual_units"] = dense["actual_units"].fillna(0)
        dense["naive_forecast"] = dense["actual_units"].shift(1)
        dense["moving_avg_forecast"] = dense["actual_units"].shift(1).rolling(7, min_periods=1).mean()
        frames.append(dense.reset_index(drop=True))
    out = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    return out.dropna(subset=["naive_forecast", "moving_avg_forecast"])


def classify_abc(total_units: pd.Series) -> pd.Series:
    ranked = total_units.sort_values(ascending=False)
    share = ranked / ranked.sum() if ranked.sum() else ranked * 0
    cumulative = share.cumsum()
    labels = pd.Series("C", index=ranked.index)
    labels[cumulative <= 0.80] = "A"
    labels[(cumulative > 0.80) & (cumulative <= 0.95)] = "B"
    return labels.reindex(total_units.index).fillna("C")


def classify_xyz(cv: pd.Series) -> pd.Series:
    return pd.cut(cv.replace([np.inf, -np.inf], np.nan).fillna(0), bins=[-0.01, 0.5, 1.0, np.inf], labels=["X", "Y", "Z"]).astype(str)


def reason_codes(row: pd.Series) -> list[str]:
    reasons: list[str] = []
    if row["abc_class"] == "A":
        reasons.append("high_volume")
    if pd.notna(row["bias_pct"]) and row["bias_pct"] <= -10:
        reasons.append("under_forecast_bias")
    if pd.notna(row["bias_pct"]) and row["bias_pct"] >= 10:
        reasons.append("over_forecast_bias")
    if pd.notna(row["wape_pct"]) and row["wape_pct"] >= 35:
        reasons.append("high_error")
    if row["xyz_class"] == "Z":
        reasons.append("volatile_demand")
    if row["reorder_point_units"] > 0 and row["safety_stock_units"] / row["reorder_point_units"] >= 0.25:
        reasons.append("replenishment_risk")
    return reasons or ["monitor"]


def recommended_action(reasons: list[str]) -> str:
    if "under_forecast_bias" in reasons or "replenishment_risk" in reasons:
        return "Review safety-stock and lead-time assumptions before replenishment decision."
    if "over_forecast_bias" in reasons:
        return "Check over-forecast pattern before increasing inventory commitment."
    if "volatile_demand" in reasons:
        return "Monitor intermittent demand and avoid automatic reorder escalation."
    return "Monitor forecast quality in next planning cycle."


def build_planner_metrics(forecasted: pd.DataFrame) -> pd.DataFrame:
    holdout_start = forecasted["date"].max() - pd.Timedelta(days=27)
    holdout = forecasted.loc[forecasted["date"] >= holdout_start].copy()
    rows = []
    for (store, item, family), g in holdout.groupby(["store_nbr", "item_nbr", "family"]):
        actual = g["actual_units"].tolist()
        naive = g["naive_forecast"].tolist()
        moving = g["moving_avg_forecast"].tolist()
        wape_m = wape(actual, moving)
        bias_m = bias_pct(actual, moving)
        avg_daily = float(np.mean(actual)) if actual else 0.0
        std_daily = float(np.std(actual, ddof=0)) if actual else 0.0
        lead_time_days = 7
        service_z = 1.28
        safety_stock = service_z * std_daily * np.sqrt(lead_time_days)
        reorder_point = avg_daily * lead_time_days + safety_stock
        rows.append(
            {
                "store_nbr": int(store),
                "item_nbr": int(item),
                "family": family,
                "actual_units": round(float(sum(actual)), 2),
                "avg_daily_units": round(avg_daily, 2),
                "wape_pct": wape_m,
                "mae_units": mae(actual, moving),
                "bias_pct": bias_m,
                "forecast_score": forecast_score(wape_m, bias_m),
                "fva_pct": fva(wape(actual, naive), wape_m),
                "demand_cv": round(std_daily / avg_daily, 2) if avg_daily else 0.0,
                "safety_stock_units": round(float(safety_stock), 2),
                "reorder_point_units": round(float(reorder_point), 2),
                "lead_time_days": lead_time_days,
                "service_level_assumption": "90% (z=1.28)",
            }
        )
    metrics = pd.DataFrame(rows)
    if metrics.empty:
        return pd.DataFrame(columns=["store_nbr", "item_nbr", "family", "actual_units", "avg_daily_units", "wape_pct", "mae_units", "bias_pct", "forecast_score", "fva_pct", "demand_cv", "safety_stock_units", "reorder_point_units", "lead_time_days", "service_level_assumption", "abc_class", "xyz_class", "reason_codes", "recommended_action", "exception_score"])
    metrics["abc_class"] = classify_abc(metrics.set_index(["store_nbr", "item_nbr"])["actual_units"]).to_numpy()
    metrics["xyz_class"] = classify_xyz(metrics["demand_cv"])
    metrics["reason_codes"] = metrics.apply(lambda r: ",".join(reason_codes(r)), axis=1)
    metrics["recommended_action"] = metrics["reason_codes"].str.split(",").apply(recommended_action)
    metrics["exception_score"] = (
        metrics["actual_units"].rank(pct=True) * 35
        + metrics["wape_pct"].fillna(0).rank(pct=True) * 25
        + metrics["bias_pct"].abs().fillna(0).rank(pct=True) * 20
        + metrics["demand_cv"].rank(pct=True) * 20
    ).round(2)
    return metrics.sort_values("exception_score", ascending=False)


def main() -> int:
    missing = missing_raw_files()
    if missing:
        print_setup_guidance(missing)
        return 0
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    demand = load_demand()
    forecasted = add_baselines(demand)
    planner_metrics = build_planner_metrics(forecasted)
    planner_metrics.to_csv(OUTPUT, index=False)
    print(f"Wrote {OUTPUT} rows={len(planner_metrics)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
