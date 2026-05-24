# Supply Chain Analytics Portfolio

Data Analytics portfolio focused on supply chain operations: delivery performance, demand signals, inventory planning, warehouse flow, outbound logistics, and decision-ready operational reporting.

This repo is built as a multi-case-study portfolio. The first featured case uses public Olist ecommerce data to show how SQL, Python, KPI design, dashboarding, and evidence-based communication can turn messy operational data into practical supply chain analytics insight.

## Featured Case Study: Olist Delivery SLA Risk

**Business question:** which delivery SLA risks deserve operations attention first?

**Analytics focus:** delivery promise performance, delay severity, customer review association, and seller/category/region investigation candidates.

**Portfolio signal:** this case demonstrates data analysis workflow, metric definition, multi-table ecommerce data modeling, operational triage, static dashboard communication, and clear limits on what public data can prove.

[![Olist Delivery SLA Risk Dashboard preview](assets/dashboard-preview.png)](https://im-khang.github.io/ai-business-data-analysis-portfolio/inventory-stockout-overstock-analysis/)

- [Live Static Dashboard](https://im-khang.github.io/ai-business-data-analysis-portfolio/inventory-stockout-overstock-analysis/)
- [Delivery SLA Summary](case-studies/inventory-stockout-overstock-analysis/artifacts/delivery-sla-summary.md)
- [Seller / Category / Region Investigation Candidates](case-studies/inventory-stockout-overstock-analysis/artifacts/seller-category-region-risk.md)
- [Review Impact Association Summary](case-studies/inventory-stockout-overstock-analysis/artifacts/review-impact-summary.md)
- [Full Olist Case Study Folder](case-studies/inventory-stockout-overstock-analysis/README.md)

### Verified Olist Snapshot

| Metric | Result |
|---|---:|
| Delivered orders analyzed | 96,470 |
| Late delivered orders | 6,534 |
| Late delivery rate | 6.77% |
| Average delivery days | 12.09 |
| Average days late among late orders | 10.62 |

### How to Read the Olist Case

- **Delivery SLA risk:** late-order volume and late rate show where service promise misses are material.
- **Customer experience signal:** review scores are associated with delivery delay bands; this is association, not proof that delay alone caused each review outcome.
- **Operations triage:** seller/category/region segments are investigation candidates, not blame assignments or root-cause proof.
- **Inventory honesty:** Olist does not include direct stock-on-hand, replenishment, warehouse availability, backorder, stockout, or overstock fields. Inventory wording in this case means fulfillment-planning proxy signal only.

## Supply Chain Analytics Roadmap

Planned future case-study directions:

- **Demand forecasting:** forecast demand patterns, quantify forecast error, and translate forecast accuracy into planning decisions.
- **Inventory management:** analyze reorder risk, service-level tradeoffs, stock coverage, aging inventory, and replenishment scenarios using datasets with real inventory fields.
- **Warehouse inbound logistics optimization:** examine inbound shipment flow, receiving bottlenecks, dock scheduling, supplier variability, and putaway readiness.
- **Outbound logistics:** analyze carrier performance, route/service levels, delivery cost drivers, last-mile risk, and fulfillment handoff performance.
- **Broader supply chain analytics:** connect procurement, fulfillment, logistics, customer experience, and operational KPIs into decision-ready dashboards and recommendations.

## Skills Demonstrated

- SQL and Python data analysis on multi-table operational datasets.
- KPI design for service levels, delay severity, customer impact signals, and triage queues.
- Data quality checks, reproducible analysis artifacts, and GitHub-ready documentation.
- Static dashboard storytelling for recruiters, hiring managers, and operations stakeholders.
- Clear distinction between evidence, proxy signals, association, and unsupported causal claims.

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
  inventory-stockout-overstock-analysis/
    index.html
    assets/
assets/
  dashboard-preview.png
```

## Data Honesty

Raw Olist CSVs are local-only and ignored by git. Public repo contains analysis code, SQL, generated aggregate dashboard data, documentation, and findings summaries. See [data setup notes](case-studies/inventory-stockout-overstock-analysis/data/README.md) for source and local placement.

For the Olist case, delivery-delay and segment patterns support fulfillment-planning investigation only. They do not directly measure inventory shortage levels, excess-stock levels, warehouse inventory, seller accountability, carrier accountability, or single-cause review impact. The current folder and GitHub Pages path keep the original `inventory-stockout-overstock-analysis` slug, but the public interpretation is delivery SLA risk with inventory proxy caveats.
