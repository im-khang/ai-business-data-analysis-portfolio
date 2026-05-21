# 📈 KPI Tree: Delivery SLA Risk & Inventory Proxy

## North Star

**Operational reliability:** protect customer trust by reducing late delivery and identifying marketplace segments that create recurring fulfillment risk.

```text
Delivery Risk Performance
├── SLA Reliability
│   ├── Late Delivery Rate
│   ├── Average Days Late
│   └── Delay Band Distribution
├── Fulfillment Performance
│   ├── Purchase-to-Approval Time
│   ├── Approval-to-Carrier Time
│   └── Carrier-to-Customer Transit Time
├── Risk Concentration
│   ├── Seller Risk
│   ├── Product Category Risk
│   ├── Customer Region Risk
│   └── Seller-to-Region Lane Risk
├── Customer Impact
│   ├── Average Review Score by Delay Band
│   └── Low Review Share for Late Orders
└── Inventory Proxy Risk
    ├── Demand Velocity
    ├── Demand Volatility
    ├── Persistent Low Demand Candidate
    └── Spike / Forecast-Risk Candidate
```

## KPI Definitions

| KPI | Formula / Logic | Source Tables | Business Interpretation | Action Path |
|---|---|---|---|---|
| Late Delivery Rate | late delivered orders / delivered orders | orders | Share of delivered orders that missed estimated delivery promise | Prioritize sellers, lanes, or categories with high late rate and meaningful volume |
| Days Late | delivered customer date - estimated delivery date | orders | Severity of missed promise | Separate minor delay noise from severe customer-impact delays |
| Total Delivery Days | delivered customer date - purchase timestamp | orders | End-to-end customer wait time | Compare experience by region/category/seller |
| Fulfillment Lead Days | delivered carrier date - approved date | orders | Time before shipment reaches carrier | Identify seller or warehouse prep bottlenecks |
| Carrier Transit Days | delivered customer date - delivered carrier date | orders | Time after carrier handoff | Identify lane/geography delivery risk |
| Review Impact | avg review score by delay band | orders, reviews | Customer trust impact of late delivery | Quantify customer-experience cost of SLA failure |
| Seller/Category/Region Risk | late rate and order volume by segment | orders, items, sellers, products, customers | Where risk concentrates operationally | Create investigation shortlist |
| Demand Velocity Proxy | average monthly orders by product/seller/category | orders, items, products | Demand intensity signal, not inventory level | Flag high-demand products needing stock availability review |
| Demand Volatility Proxy | variation in monthly orders | orders, items, products | Forecast difficulty signal | Flag products/categories needing planning review |
| Overstock Proxy Candidate | persistent low order volume across active months | orders, items, products | Possible slow-moving item signal, not confirmed overstock | Requires stock-on-hand and holding-cost data before action |

## Decision Rule

High-priority operational segments should combine:

1. meaningful order volume,
2. high late delivery rate,
3. high days-late severity,
4. customer review impact, and
5. clear owner path: seller management, fulfillment process, carrier lane, category planning, or inventory review.
