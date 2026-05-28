# 🚚 Olist Delivery Risk & Inventory Proxy Case Study

This case study analyzes **ecommerce fulfillment and delivery SLA risk** using the public Olist Brazilian E-Commerce dataset. It is not a generic sales dashboard. The goal is to show where marketplace delivery risk concentrates across sellers, product categories, customer regions, and order patterns, then explain what operations teams should investigate first.

## 🎯 Business Question

Which sellers, categories, regions, and order patterns create the highest delivery SLA risk, how does late delivery affect customer review outcomes, and what inventory-risk proxy signals can be identified without claiming direct stockout/overstock certainty?

## 🧭 Reviewer Guide

Start here:

1. [Live Static Dashboard](https://im-khang.com/cases/olist-delivery-sla-risk/) — production portfolio view of aggregate delivery SLA findings.
2. `artifacts/kpi-tree.md` — KPI definitions, business interpretation, and action paths.
3. `artifacts/assumptions.md` — data limitations and inventory proxy rules.
4. `sql/00_schema_overview.sql` — source table map and join logic.
5. `sql/01_delivery_sla_metrics.sql` — order-level delivery KPI logic.
6. `sql/02_seller_category_region_risk.sql` — seller/category/geography risk segmentation.
7. `sql/03_inventory_proxy_metrics.sql` — demand velocity proxy logic with limitations.
8. `notebooks/01_olist_delivery_risk_foundation.py` — runnable pandas foundation script.

## 📦 Data Setup

Download the public Olist dataset from Kaggle:

<https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce>

Place CSV files in:

```text
case-studies/inventory-stockout-overstock-analysis/data/raw/
```

See `data/README.md` for exact filenames and folder policy. Raw CSVs and generated outputs are ignored by git.

Create a local Python environment and install pandas:

```bash
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip pandas
```

## ▶️ Run Order

From repo root:

```bash
python case-studies/inventory-stockout-overstock-analysis/notebooks/01_olist_delivery_risk_foundation.py
```

If data is missing, the script prints clear setup guidance. If data is present, it loads core tables, validates required columns, creates delivery timing metrics, and prints first summary tables.

## 📊 Analysis Foundation

The foundation covers:

- delivery promise vs actual delivery date
- late delivery rate and days-late bands
- fulfillment lead time and carrier transit time
- seller/category/customer-region risk segmentation
- optional review-score impact when reviews data is available
- demand velocity and volatility as inventory-risk proxy signals

## ⚠️ Inventory Proxy Limitation

Olist does **not** include stock-on-hand, replenishment, warehouse availability, purchase orders, or backorder fields. This project therefore does not claim direct stockout or overstock measurement. Inventory risk is framed as proxy analysis using demand velocity, volatility, category/seller patterns, and delivery performance.

Production-grade inventory decisions would require additional company data such as inventory snapshots, lead times, supplier constraints, replenishment orders, warehouse capacity, and lost-sales records.
