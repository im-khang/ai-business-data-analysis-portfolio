# Supply Chain Analytics Portfolio

<p align="center">
  <strong>Data Analytics portfolio for supply chain operations</strong><br>
  Delivery performance · demand signals · inventory planning · warehouse flow · outbound logistics · control tower reporting
</p>

<p align="center">
  <a href="https://im-khang.github.io/ai-business-data-analysis-portfolio/">Portfolio Homepage</a> ·
  <a href="https://im-khang.github.io/ai-business-data-analysis-portfolio/inventory-stockout-overstock-analysis/">Live Olist Dashboard</a> ·
  <a href="case-studies/inventory-stockout-overstock-analysis/README.md">Featured Case Study</a> ·
  <a href="case-studies/inventory-stockout-overstock-analysis/artifacts/delivery-sla-summary.md">SLA Evidence</a>
</p>

<p align="center">
  <strong>SQL analysis</strong> ·
  <strong>Python data prep</strong> ·
  <strong>GitHub Pages dashboard</strong> ·
  <strong>Supply chain operations analytics</strong> ·
  <strong>Evidence-bounded claims</strong>
</p>

## Featured Work: Olist Delivery SLA Risk

| Case | Decision question | Portfolio proof | Links |
|---|---|---|---|
| **Olist Delivery SLA Risk** | Which delivery SLA risks deserve operations attention first? | Multi-table ecommerce analysis, KPI design, delay-severity triage, review-score association, seller/category/region investigation queue, and caveat-controlled recommendation writing. | [Live dashboard](https://im-khang.github.io/ai-business-data-analysis-portfolio/inventory-stockout-overstock-analysis/) · [Case study](case-studies/inventory-stockout-overstock-analysis/README.md) · [SLA summary](case-studies/inventory-stockout-overstock-analysis/artifacts/delivery-sla-summary.md) · [Candidate ranking](case-studies/inventory-stockout-overstock-analysis/artifacts/seller-category-region-risk.md) |

[![Olist Delivery SLA Risk Dashboard preview](assets/dashboard-preview.png)](https://im-khang.github.io/ai-business-data-analysis-portfolio/inventory-stockout-overstock-analysis/)

### KPI Snapshot

| Delivered orders analyzed | Late delivered orders | Late delivery rate | Avg delivery days | Avg days late among late orders |
|---:|---:|---:|---:|---:|
| 96,470 | 6,534 | 6.77% | 12.09 | 10.62 |

### Why this case matters

- **Delivery SLA risk:** late-order volume and late rate show where service promise misses are material.
- **Customer experience signal:** review scores are associated with delivery delay bands; this is association, not proof that delay alone caused each review outcome.
- **Operations triage:** seller/category/region segments are investigation candidates, not blame assignments or root-cause proof.
- **Decision discipline:** recommendations stay tied to available evidence and call for internal inventory, fulfillment, and carrier data before production policy changes.

## Portfolio Roadmap

| Pillar | Future case-study direction | Decision value |
|---|---|---|
| **Demand forecasting** | Forecast demand patterns, quantify forecast error, and translate accuracy into planning decisions. | Improve planning confidence and exception handling. |
| **Inventory management** | Analyze reorder risk, service-level tradeoffs, stock coverage, aging inventory, and replenishment scenarios using datasets with real inventory fields. | Balance availability, working capital, and risk. |
| **Warehouse inbound logistics optimization** | Examine inbound shipment flow, receiving bottlenecks, dock scheduling, supplier variability, and putaway readiness. | Reduce receiving friction and improve readiness. |
| **Outbound logistics** | Analyze carrier performance, route/service levels, delivery cost drivers, last-mile risk, and fulfillment handoff performance. | Prioritize lanes, partners, and service levels. |
| **Control tower / broader supply chain analytics** | Connect procurement, fulfillment, logistics, customer experience, and operational KPIs into decision-ready dashboards. | Turn fragmented signals into operating decisions. |

## Skills Demonstrated

- SQL and Python analysis on multi-table operational datasets.
- KPI design for service levels, delay severity, customer impact signals, and triage queues.
- Data quality checks, reproducible analysis artifacts, and GitHub-ready documentation.
- Static dashboard storytelling for recruiters, hiring managers, and operations stakeholders.
- Clear separation between evidence, proxy signals, association, and unsupported causal claims.

## Repository Structure

```text
case-studies/
  inventory-stockout-overstock-analysis/
    README.md
    artifacts/
      delivery-sla-summary.md
      seller-category-region-risk.md
      review-impact-summary.md
      stakeholder-map.md
      requirements.md
      kpi-tree.md
      process-flow.md
      assumptions.md
    sql/
    notebooks/
    data/
    dashboard/
docs/
  index.html
  assets/css/site.css
  inventory-stockout-overstock-analysis/
    index.html
    assets/
assets/
  dashboard-preview.png
```

## Data Honesty

Raw Olist CSVs are local-only and ignored by git. Public repo contains analysis code, SQL, generated aggregate dashboard data, documentation, and findings summaries. See [data setup notes](case-studies/inventory-stockout-overstock-analysis/data/README.md) for source and local placement.

For the Olist case, delivery-delay and segment patterns support fulfillment-planning investigation only. They do not directly measure inventory shortage levels, excess-stock levels, warehouse inventory, seller accountability, carrier accountability, or single-cause review impact. The current folder and GitHub Pages path keep the original `inventory-stockout-overstock-analysis` slug, but the public interpretation is delivery SLA risk with inventory proxy caveats.
