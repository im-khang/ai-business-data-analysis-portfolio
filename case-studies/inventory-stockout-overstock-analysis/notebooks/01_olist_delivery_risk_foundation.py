# %%
"""Olist delivery risk foundation script.

Run from repo root:
    python case-studies/inventory-stockout-overstock-analysis/notebooks/01_olist_delivery_risk_foundation.py

This notebook-style script validates local CSV placement, loads core Olist tables,
creates delivery SLA metrics, and prints starter summary tables.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd
else:
    pd = None

CASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = CASE_DIR / "data" / "raw"
DATA_SOURCE = "https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce"

REQUIRED_FILES = {
    "orders": "olist_orders_dataset.csv",
    "items": "olist_order_items_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "products": "olist_products_dataset.csv",
}

OPTIONAL_FILES = {
    "reviews": "olist_order_reviews_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}

REQUIRED_COLUMNS = {
    "orders": {
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    },
    "items": {"order_id", "order_item_id", "product_id", "seller_id", "price", "freight_value"},
    "customers": {"customer_id", "customer_city", "customer_state"},
    "sellers": {"seller_id", "seller_city", "seller_state"},
    "products": {"product_id", "product_category_name"},
    "reviews": {"order_id", "review_score"},
}


def print_missing_file_guidance(missing: Iterable[str]) -> None:
    """Print clear setup guidance when raw Olist files are absent."""
    missing = list(missing)
    print("Missing required Olist CSV files.")
    print(f"Target folder: {RAW_DIR}")
    print(f"Download source: {DATA_SOURCE}")
    print("Expected required filenames:")
    for name in REQUIRED_FILES.values():
        marker = "MISSING" if name in missing else "OK"
        print(f"  - {name} [{marker}]")
    print("Optional filenames:")
    for name in OPTIONAL_FILES.values():
        print(f"  - {name}")


def validate_columns(table_name: str, frame: pd.DataFrame) -> None:
    """Validate required source columns before KPI logic runs."""
    expected = REQUIRED_COLUMNS.get(table_name, set())
    missing = sorted(expected.difference(frame.columns))
    if missing:
        raise ValueError(f"{table_name} missing required columns: {missing}")


def load_csvs() -> dict[str, pd.DataFrame] | None:
    """Load Olist CSVs if present; return None when setup guidance should be shown."""
    missing = [filename for filename in REQUIRED_FILES.values() if not (RAW_DIR / filename).exists()]
    if missing:
        print_missing_file_guidance(missing)
        return None

    global pd
    try:
        import pandas as pandas_module
        pd = pandas_module
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "pandas is required after Olist CSVs are present. Install pandas in your local analysis environment, then rerun."
        ) from exc

    frames: dict[str, pd.DataFrame] = {}
    def read_olist_csv(path: Path) -> pd.DataFrame:
        try:
            return pd.read_csv(path, encoding="utf-8")
        except UnicodeDecodeError:
            return pd.read_csv(path, encoding="latin1")
        except pd.errors.EmptyDataError as exc:
            raise ValueError(f"{path.name} is empty; replace it with the downloaded Olist CSV.") from exc
        except pd.errors.ParserError as exc:
            raise ValueError(f"{path.name} is malformed; verify the Kaggle download and CSV extraction.") from exc

    for table_name, filename in REQUIRED_FILES.items():
        frames[table_name] = read_olist_csv(RAW_DIR / filename)
        validate_columns(table_name, frames[table_name])

    for table_name, filename in OPTIONAL_FILES.items():
        path = RAW_DIR / filename
        if path.exists():
            frames[table_name] = read_olist_csv(path)
            if table_name in REQUIRED_COLUMNS:
                validate_columns(table_name, frames[table_name])
        else:
            print(f"Warning: optional file unavailable; skipping {filename}")

    return frames


# %%
def build_delivery_metrics(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Create order-level delivery SLA metrics from Olist timestamp columns."""
    orders = frames["orders"].copy()
    timestamp_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in timestamp_cols:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

    delivered = orders.loc[
        (orders["order_status"] == "delivered")
        & orders["order_delivered_customer_date"].notna()
        & orders["order_estimated_delivery_date"].notna()
        & orders["order_purchase_timestamp"].notna()
    ].copy()

    if delivered.empty:
        print("No delivered orders with purchase, delivery, and estimate dates. No SLA metrics available.")
        return delivered

    null_metric_inputs = delivered[["order_approved_at", "order_delivered_carrier_date"]].isna().sum()
    if null_metric_inputs.any():
        print("Warning: fulfillment/carrier metrics have null timestamp inputs:")
        print(null_metric_inputs[null_metric_inputs > 0].to_string())

    delivered["total_delivery_days"] = (
        delivered["order_delivered_customer_date"] - delivered["order_purchase_timestamp"]
    ).dt.days
    delivered["fulfillment_lead_days"] = (
        delivered["order_delivered_carrier_date"] - delivered["order_approved_at"]
    ).dt.days
    delivered["carrier_transit_days"] = (
        delivered["order_delivered_customer_date"] - delivered["order_delivered_carrier_date"]
    ).dt.days
    delivered["days_late"] = (
        delivered["order_delivered_customer_date"] - delivered["order_estimated_delivery_date"]
    ).dt.days
    delivered["late_delivery_flag"] = delivered["days_late"].gt(0)
    delivered["delay_band"] = pd.cut(
        delivered["days_late"],
        bins=[float("-inf"), 0, 3, 7, 14, float("inf")],
        labels=["On time / early", "1-3 days late", "4-7 days late", "8-14 days late", "15+ days late"],
    ).cat.add_categories(["Unknown"]).fillna("Unknown")
    return delivered


# %%
def print_summary_tables(frames: dict[str, pd.DataFrame], delivery: pd.DataFrame) -> None:
    """Print first summary tables for portfolio reviewer inspection."""
    if delivery.empty:
        print("\n=== Delivery SLA Summary ===")
        print("No delivery metrics available after date/status filters.")
        return

    print("\n=== Delivery SLA Summary ===")
    print(
        pd.DataFrame(
            {
                "delivered_orders": [len(delivery)],
                "late_orders": [int(delivery["late_delivery_flag"].sum())],
                "late_delivery_rate_pct": [round(delivery["late_delivery_flag"].mean() * 100, 2)],
                "avg_total_delivery_days": [round(delivery["total_delivery_days"].mean(), 2)],
                "avg_days_late": [round(delivery.loc[delivery["late_delivery_flag"], "days_late"].mean(), 2) if delivery["late_delivery_flag"].any() else 0.0],
            }
        ).to_string(index=False)
    )

    print("\n=== Delay Band Distribution ===")
    print(delivery["delay_band"].value_counts(dropna=False).sort_index().to_string())

    items = frames["items"]
    sellers = frames["sellers"]
    products = frames["products"]
    customers = frames["customers"]

    segment = (
        delivery[["order_id", "customer_id", "late_delivery_flag", "days_late"]]
        .merge(items, on="order_id", how="inner")
        .merge(sellers[["seller_id", "seller_state"]], on="seller_id", how="left")
        .merge(products[["product_id", "product_category_name"]], on="product_id", how="left")
        .merge(customers[["customer_id", "customer_state"]], on="customer_id", how="left")
    )

    segment[["price", "freight_value"]] = segment[["price", "freight_value"]].apply(pd.to_numeric, errors="coerce")
    segment["gross_item_value"] = segment["price"].fillna(0) + segment["freight_value"].fillna(0)

    # Risk severity should average lateness only across late orders; averaging early orders can hide delay pain.
    risk_summary = (
        segment.assign(days_late_for_late_orders=segment["days_late"].where(segment["late_delivery_flag"]))
        .groupby(["seller_state", "customer_state", "product_category_name"], dropna=False)
        .agg(
            orders=("order_id", "nunique"),
            late_rate_pct=("late_delivery_flag", lambda s: round(float(s.mean() * 100), 2)),
            avg_days_late_late_orders=("days_late_for_late_orders", "mean"),
            gross_item_value=("gross_item_value", "sum"),
        )
        .reset_index()
        .query("orders >= 10")
        .sort_values(["late_rate_pct", "orders"], ascending=[False, False])
        .head(10)
    )
    print("\n=== Top Seller/Customer/Category Risk Segments ===")
    if risk_summary.empty:
        print("No segment has at least 10 orders in current data sample.")
    else:
        print(risk_summary.to_string(index=False))

    if "reviews" in frames:
        reviews = frames["reviews"][["order_id", "review_score"]].dropna(subset=["order_id"]).drop_duplicates("order_id")
        reviews["review_score"] = pd.to_numeric(reviews["review_score"], errors="coerce")
        dropped_review_scores = int(reviews["review_score"].isna().sum())
        if dropped_review_scores:
            print(f"Warning: dropped {dropped_review_scores} reviews with nonnumeric review_score.")
        reviews = reviews.dropna(subset=["review_score"])
        if reviews.empty:
            print("\n=== Review Impact ===")
            print("Skipped: optional reviews data has no numeric review_score values.")
            return
        review_impact = (
            delivery[["order_id", "late_delivery_flag", "delay_band"]]
            .merge(reviews, on="order_id", how="inner")
            .groupby(["delay_band", "late_delivery_flag"], dropna=False)
            .agg(orders=("order_id", "nunique"), avg_review_score=("review_score", "mean"))
            .reset_index()
        )
        print("\n=== Review Impact by Delay Band ===")
        print(review_impact.to_string(index=False))
    else:
        print("\n=== Review Impact ===")
        print("Skipped: optional olist_order_reviews_dataset.csv unavailable.")

    print("\nInventory proxy note: Olist lacks stock-on-hand/replenishment fields. Use demand velocity and volatility only as proxy signals.")


# %%
def main() -> int:
    frames = load_csvs()
    if frames is None:
        return 0
    delivery = build_delivery_metrics(frames)
    print_summary_tables(frames, delivery)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
