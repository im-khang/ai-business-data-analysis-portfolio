# ⚠️ Assumptions & Data Limitations

## Dataset Scope

This project uses the public **Olist Brazilian E-Commerce Public Dataset**. It is suitable for delivery SLA, marketplace seller, category, geography, customer review, and payment-pattern analysis.

## Inventory Proxy Rule

Olist does **not** provide direct inventory fields such as:

- stock-on-hand quantity
- replenishment orders
- warehouse availability
- supplier lead time
- backorders
- lost sales from unavailable products
- carrying cost or markdown cost

Therefore this project must not claim direct stockout rate, overstock value, inventory turnover, or days of inventory on hand.

## What Can Be Inferred

Inventory-risk proxy signals can be created from:

- product/category demand velocity
- monthly demand volatility
- seller/category order concentration
- repeated demand spikes
- persistent low-demand products
- delivery delays that may suggest fulfillment strain

These are **investigation signals**, not final inventory decisions.

## What Production Analysis Would Need

A production-grade stockout/overstock model would require:

- daily inventory snapshots by SKU/location
- replenishment orders and receipt dates
- supplier and warehouse lead times
- demand forecasts
- lost-sales or stockout event logs
- holding cost, markdown cost, and service-level targets

## Review Data Assumption

`olist_order_reviews_dataset.csv` is optional for script execution. If unavailable, delivery metrics still run and review-impact analysis is skipped with a warning.

## Business Framing Assumption

This case is framed for ecommerce operations, marketplace management, fulfillment/logistics stakeholders, and BA/DA interview reviewers. Technical outputs should remain tied to operational decisions, not descriptive dashboard decoration.
