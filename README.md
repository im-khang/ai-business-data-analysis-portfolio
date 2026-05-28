# AI-Augmented Business Analytics Portfolio

<p align="center">
  <strong>Multi-case analytics portfolio for supply-chain and operations decisions</strong><br>
  Demand planning · delivery SLA risk · replenishment review · evidence boundaries · decision storytelling
</p>

<p align="center">
  <a href="https://im-khang.com/">Portfolio Homepage</a> ·
  <a href="https://im-khang.com/cases/favorita-planner-exception-queue/">Favorita Dashboard</a> ·
  <a href="https://im-khang.com/cases/olist-delivery-sla-risk/">Olist Dashboard</a> ·
  <a href="case-studies/demand-forecasting-replenishment/README.md">Favorita Case</a> ·
  <a href="case-studies/inventory-stockout-overstock-analysis/README.md">Olist Case</a>
</p>

<p align="center">
  <strong>AI as thinking partner</strong> ·
  <strong>Human-owned analysis logic</strong> ·
  <strong>SQL/Python evidence</strong> ·
  <strong>Static dashboard products</strong> ·
  <strong>Caveat-safe recommendations</strong>
</p>

## What this repository is

This is a growing AI-augmented analytics portfolio: public case studies, dashboards, and artifacts that show how business questions become decision-ready evidence.

AI is used as a thinking partner and drafting accelerator. Human judgment owns problem framing, metric logic, validation, interpretation, caveats, and recommendations. Claims stay bounded by available data.

## Portfolio Cases

| Case | Decision question | Portfolio proof | Links |
|---|---|---|---|
| **Favorita Demand Forecasting & Replenishment Review** | Which item/store/family combinations deserve planner attention first? | Forecast accuracy metrics, WAPE/MAE/Bias %, Forecast Score, FVA framing, ABC/XYZ segmentation, planner queue, transparent replenishment assumptions. | [Live dashboard](https://im-khang.com/cases/favorita-planner-exception-queue/) · [Case study](case-studies/demand-forecasting-replenishment/README.md) · [Build metadata](docs/demand-forecasting-replenishment/assets/data/build_metadata.json) |
| **Olist Delivery SLA Risk** | Which delivery SLA risks deserve operations attention first? | Multi-table ecommerce analysis, KPI design, delay-severity triage, review-score association, seller/category/region investigation queue, caveat-controlled recommendation writing. | [Live dashboard](https://im-khang.com/cases/olist-delivery-sla-risk/) · [Case study](case-studies/inventory-stockout-overstock-analysis/README.md) · [SLA summary](case-studies/inventory-stockout-overstock-analysis/artifacts/delivery-sla-summary.md) · [Candidate ranking](case-studies/inventory-stockout-overstock-analysis/artifacts/seller-category-region-risk.md) |

[![Portfolio dashboard preview](assets/dashboard-preview.png)](https://im-khang.com/)

## Operating System for Each Case

1. **Stakeholder pain** — name planning, logistics, or operations friction.
2. **Decision question** — convert vague issue into answerable question.
3. **Evidence model** — use SQL/Python metrics, aggregate data, and reproducible artifacts.
4. **Caveat boundary** — separate proxy, association, assumption, and unsupported causality.
5. **Recommendation** — propose next action that fits evidence strength.
6. **Interview prompt** — expose what I would validate next with internal systems.

## Interview Discussion Prompts

- How would I redesign metrics if direct stock-on-hand, purchase orders, carrier scans, or supplier lead-time data became available?
- Which public-data claims are safe, and which require internal operational validation?
- How should planners prioritize forecast error, volume, bias, and variability when queue capacity is limited?
- How would I turn static dashboard findings into stakeholder meeting agenda, acceptance criteria, or follow-up analysis plan?

## Roadmap

| Portfolio pillar | Future case-study direction | Decision value |
|---|---|---|
| **Demand planning** | More forecasting baselines, promotional effects, forecast bias monitoring, and exception governance. | Improve planning confidence and exception handling. |
| **Inventory management** | Reorder risk, service-level tradeoffs, stock coverage, aging inventory, and replenishment scenarios using datasets with real inventory fields. | Balance availability, working capital, and risk. |
| **Warehouse operations** | Inbound flow, receiving bottlenecks, dock scheduling, supplier variability, and putaway readiness. | Reduce warehouse friction and improve readiness. |
| **Outbound logistics** | Carrier performance, route/service levels, delivery cost drivers, last-mile risk, and fulfillment handoffs. | Prioritize lanes, partners, and service levels. |
| **Control tower analytics** | Connect procurement, fulfillment, logistics, customer experience, and operational KPIs into decision-ready dashboards. | Turn fragmented signals into operating decisions. |

## Repository Structure

```text
case-studies/
  demand-forecasting-replenishment/
  inventory-stockout-overstock-analysis/
docs/
  index.html
  assets/css/site.css
  assets/js/registry.js
  assets/js/render-cards.js
  demand-forecasting-replenishment/
  inventory-stockout-overstock-analysis/
assets/
  dashboard-preview.png
```

## Data Honesty

Raw source data stays local-only and ignored by git. Public repo contains analysis code, SQL, generated aggregate dashboard data, documentation, and findings summaries.

Olist delivery-delay and segment patterns support fulfillment-planning investigation only. They do not directly measure inventory shortage levels, excess-stock levels, warehouse inventory, seller accountability, carrier accountability, or single-cause review impact. Favorita outputs are planner-review candidates and transparent assumptions, not production replenishment instructions.
