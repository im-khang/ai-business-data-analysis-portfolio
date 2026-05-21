# 🚚 Delivery SLA Summary

## Headline finding

Olist delivered **96,470 orders** in the analyzed dataset. **6,534 delivered orders arrived late**, producing a **6.77% late delivery rate**. Average end-to-end delivery time was **12.09 days**, and late orders were late by **10.62 days on average**.

This means delivery risk is not universal across all orders. Combined with the seller/category/region artifact, the evidence suggests risk concentrates in investigation lanes; when failures happen, delay severity is large enough to affect customer review outcomes and operational workload.

## Evidence table

| KPI | Value | Business meaning |
|---|---:|---|
| Delivered orders | 96,470 | Base population for SLA analysis |
| Late delivered orders | 6,534 | Orders that missed estimated delivery promise |
| Late delivery rate | 6.77% | Share of delivered orders with SLA miss |
| Average total delivery days | 12.09 | Average purchase-to-customer delivery time |
| Average days late | 10.62 | Average severity among late orders |

## Delay-band distribution

| Delay band | Orders | Interpretation |
|---|---:|---|
| On time / early | 89,936 | Majority of delivered orders met or beat promise |
| 1-3 days late | 1,870 | Minor misses; monitor for preventable process noise |
| 4-7 days late | 1,802 | Moderate misses; likely visible customer impact |
| 8-14 days late | 1,478 | Severe misses; investigate fulfillment/carrier path |
| 15+ days late | 1,384 | Critical misses; prioritize root-cause review |
| Unknown | 0 | Delay banding covered all delivered orders in current run |

## Business interpretation

- **SLA reliability:** A 6.77% late rate suggests most orders work, but risk concentrates in specific seller/category/region lanes rather than requiring broad generic fixes.
- **Severity:** Average late severity of 10.62 days means late orders are not only slightly late; many misses are operationally meaningful.
- **Priority:** Investigations should focus on high-volume segments with high late rate and high days-late severity, not on isolated one-off misses.

## Recommended next actions

1. Prioritize seller/category/region lanes with meaningful order volume and high late rate.
2. Separate fulfillment-delay causes from carrier-transit/geography causes where timestamp completeness allows.
3. Track severe delay bands (`8-14 days late`, `15+ days late`) as review-outcome priority groups.
4. Use demand velocity and volatility only as inventory-risk proxy signals; Olist does not contain stock-on-hand, replenishment, or backorder fields.

## Caveats

The foundation run warned that fulfillment/carrier metrics have limited null timestamp inputs: `order_approved_at` has 14 nulls and `order_delivered_carrier_date` has 1 null. These gaps are small relative to delivered-order volume, but any detailed fulfillment-stage diagnosis should preserve null-handling rules.

This artifact does **not** claim direct measured inventory outcomes or replenishment performance. Inventory language here means proxy/investigation signal only.
