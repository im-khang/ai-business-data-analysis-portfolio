"""Export aggregate-only Olist delivery SLA dashboard data for GitHub Pages."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
CASE_DIR = ROOT / "case-studies" / "inventory-stockout-overstock-analysis"
RAW_DIR = CASE_DIR / "data" / "raw"
OUT_DIR = ROOT / "docs" / "inventory-stockout-overstock-analysis" / "assets" / "data"

REQUIRED_FILES = {
    "orders": "olist_orders_dataset.csv",
    "items": "olist_order_items_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}

REQUIRED_COLUMNS = {
    "orders": {"order_id", "customer_id", "order_status", "order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"},
    "items": {"order_id", "order_item_id", "product_id", "seller_id", "price", "freight_value"},
    "customers": {"customer_id", "customer_state"},
    "sellers": {"seller_id", "seller_state"},
    "products": {"product_id", "product_category_name"},
    "reviews": {"order_id", "review_score"},
    "category_translation": {"product_category_name", "product_category_name_english"},
}


def load_csv(name: str, filename: str) -> pd.DataFrame:
    path = RAW_DIR / filename
    if not path.exists():
        raise FileNotFoundError(filename)
    try:
        frame = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        frame = pd.read_csv(path, encoding="latin1")
    missing = REQUIRED_COLUMNS[name] - set(frame.columns)
    if missing:
        raise ValueError(f"{filename} missing columns: {', '.join(sorted(missing))}")
    return frame


def load_frames() -> dict[str, pd.DataFrame]:
    missing = [filename for filename in REQUIRED_FILES.values() if not (RAW_DIR / filename).exists()]
    if missing:
        message = [
            "Missing required Olist raw CSV files.",
            f"Place files in: {RAW_DIR.relative_to(ROOT)}",
            "Download source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce",
            "Missing:",
            *[f"- {name}" for name in missing],
        ]
        raise FileNotFoundError("\n".join(message))
    return {name: load_csv(name, filename) for name, filename in REQUIRED_FILES.items()}


def to_records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    return json.loads(frame.to_json(orient="records", date_format="iso"))


def pct(series: pd.Series) -> float:
    if len(series) == 0:
        return 0.0
    return round(float(series.mean() * 100), 2)


def build_delivery(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    orders = frames["orders"].copy()
    for column in ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]:
        orders[column] = pd.to_datetime(orders[column], errors="coerce")
    delivered = orders.loc[orders["order_status"].eq("delivered")].dropna(
        subset=["order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"]
    ).copy()
    delivered["delivery_days"] = (delivered["order_delivered_customer_date"] - delivered["order_purchase_timestamp"]).dt.total_seconds() / 86400
    delivered["days_late"] = (delivered["order_delivered_customer_date"] - delivered["order_estimated_delivery_date"]).dt.total_seconds() / 86400
    delivered["late_delivery_flag"] = delivered["days_late"] > 0
    delivered["days_late_positive"] = delivered["days_late"].clip(lower=0)
    delivered["delay_band"] = pd.cut(
        delivered["days_late"],
        bins=[float("-inf"), 0, 3, 7, 14, float("inf")],
        labels=["On time / early", "1-3 days late", "4-7 days late", "8-14 days late", "15+ days late"],
        include_lowest=True,
    )
    delivered["purchase_month"] = delivered["order_purchase_timestamp"].dt.to_period("M").astype(str)
    return delivered


def write_json(name: str, data: Any) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_outputs(frames: dict[str, pd.DataFrame]) -> dict[str, Any]:
    delivery = build_delivery(frames)
    if delivery.empty:
        raise ValueError("No delivered orders available after required date filters.")

    late = delivery["late_delivery_flag"]
    late_orders = int(late.sum())
    delivered_orders = int(delivery["order_id"].nunique())
    avg_days_late_late = float(delivery.loc[late, "days_late_positive"].mean()) if late_orders else 0.0

    kpis = {
        "delivered_orders": delivered_orders,
        "late_orders": late_orders,
        "late_delivery_rate_pct": pct(late),
        "avg_delivery_days": round(float(delivery["delivery_days"].mean()), 2),
        "avg_days_late_late_orders": round(avg_days_late_late, 2),
        "positioning_note": "Inventory language is proxy-only: Olist lacks direct inventory, replenishment, warehouse availability, and backorder fields.",
    }

    delay_bands = (
        delivery.groupby("delay_band", observed=False)
        .agg(orders=("order_id", "nunique"), avg_days_late=("days_late_positive", "mean"))
        .reset_index()
    )
    delay_bands["order_share_pct"] = (delay_bands["orders"] / delivered_orders * 100).round(2)
    delay_bands["avg_days_late"] = delay_bands["avg_days_late"].round(2)
    delay_bands["delay_band"] = delay_bands["delay_band"].astype(str)

    reviews = frames["reviews"][["order_id", "review_score"]].drop_duplicates("order_id").copy()
    reviews["review_score"] = pd.to_numeric(reviews["review_score"], errors="coerce")
    review_impact = (
        delivery[["order_id", "delay_band", "late_delivery_flag"]]
        .merge(reviews.dropna(subset=["review_score"]), on="order_id", how="inner")
        .groupby(["delay_band", "late_delivery_flag"], observed=True)
        .agg(orders=("order_id", "nunique"), avg_review_score=("review_score", "mean"))
        .reset_index()
    )
    review_impact = review_impact[review_impact["orders"] > 0].copy()
    review_impact["delay_band"] = review_impact["delay_band"].astype(str)
    review_impact["avg_review_score"] = review_impact["avg_review_score"].round(2)

    items = frames["items"].copy()
    items["price"] = pd.to_numeric(items["price"], errors="coerce").fillna(0)
    items["freight_value"] = pd.to_numeric(items["freight_value"], errors="coerce").fillna(0)
    products = frames["products"][["product_id", "product_category_name"]]
    translation = frames["category_translation"]
    products = products.merge(translation, on="product_category_name", how="left")
    products["category"] = products["product_category_name_english"].fillna(products["product_category_name"]).fillna("Unknown")
    enriched = (
        items.merge(delivery[["order_id", "customer_id", "late_delivery_flag", "days_late_positive"]], on="order_id", how="inner")
        .merge(frames["sellers"][["seller_id", "seller_state"]], on="seller_id", how="left")
        .merge(products[["product_id", "category"]], on="product_id", how="left")
        .merge(frames["customers"][["customer_id", "customer_state"]], on="customer_id", how="left")
    )
    enriched["gross_value"] = enriched["price"] + enriched["freight_value"]
    segment_orders = enriched.drop_duplicates(["seller_state", "customer_state", "category", "order_id"]).copy()
    risk_segments = (
        segment_orders.groupby(["seller_state", "customer_state", "category"], dropna=False)
        .agg(
            orders=("order_id", "nunique"),
            late_orders=("late_delivery_flag", "sum"),
            avg_days_late_late_orders=("days_late_positive", lambda s: float(s[s > 0].mean()) if (s > 0).any() else 0.0),
        )
        .reset_index()
    )
    segment_value = (
        enriched.groupby(["seller_state", "customer_state", "category"], dropna=False)
        .agg(gross_value=("gross_value", "sum"))
        .reset_index()
    )
    risk_segments = risk_segments.merge(segment_value, on=["seller_state", "customer_state", "category"], how="left")
    risk_segments = risk_segments[risk_segments["orders"] >= 30].copy()
    risk_segments["late_rate_pct"] = (risk_segments["late_orders"] / risk_segments["orders"] * 100).round(2)
    risk_segments["avg_days_late_late_orders"] = risk_segments["avg_days_late_late_orders"].round(2)
    risk_segments["gross_value"] = risk_segments["gross_value"].round(2)
    risk_segments = risk_segments.sort_values(["late_orders", "late_rate_pct", "avg_days_late_late_orders"], ascending=False).head(15)

    monthly = (
        delivery.groupby("purchase_month")
        .agg(orders=("order_id", "nunique"), late_rate_pct=("late_delivery_flag", lambda s: round(float(s.mean() * 100), 2)), avg_delivery_days=("delivery_days", "mean"))
        .reset_index()
    )
    monthly = monthly[monthly["orders"] >= 30].copy()
    monthly["avg_delivery_days"] = monthly["avg_delivery_days"].round(2)

    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "Olist Brazilian E-Commerce public dataset",
        "privacy_note": "Aggregate dashboard data only; raw CSVs stay local and ignored by git.",
        "row_level_export": False,
        "files": sorted(REQUIRED_FILES.values()),
    }

    return {
        "kpis.json": kpis,
        "delay_bands.json": to_records(delay_bands),
        "review_impact.json": to_records(review_impact),
        "risk_segments.json": to_records(risk_segments),
        "monthly_sla_trend.json": to_records(monthly),
        "build_metadata.json": metadata,
    }


def main() -> int:
    try:
        outputs = build_outputs(load_frames())
        for name, data in outputs.items():
            write_json(name, data)
    except Exception as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"Wrote {len(outputs)} aggregate JSON files to {OUT_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
