# 🧭 Seller / Category / Region Risk Prioritization

## Headline finding

Delivery SLA risk concentrates in specific seller, customer-region, and category combinations. These rows are **exploratory investigation candidates**, not final policy decisions, because the table uses a minimum threshold of only 10 orders per segment.

## Method note

Segments are calculated at order level by `seller_id`, seller state, customer state, and product category. Late rate uses `late_orders / orders`, so percentages reconcile to integer late-order counts. Gross item value sums item price plus freight within each segment.

## Top exploratory risk segments from real-data foundation inputs

| Seller ID | Seller state | Customer state | Product category | Orders | Late orders | Late rate | Avg days late among late orders | Gross item value |
|---|---|---|---|---:|---:|---:|---:|---:|
| 835f0f7810c76831d6c7d24c7a646d4d | SP | SP | utilidades_domesticas | 10 | 7 | 70.00% | 2.80 | 1,192.07 |
| 2c9e548be18521d1c43cde1c582c6de8 | SP | RJ | papelaria | 14 | 8 | 57.14% | 22.75 | 825.60 |
| 06a2c3af7b3aee5d69171b0e14f0ee87 | MA | ES | beleza_saude | 13 | 7 | 53.85% | 12.83 | 1,506.33 |
| e5a3438891c0bfdb9394643f95273d8e | SP | RJ | fashion_bolsas_e_acessorios | 13 | 7 | 53.85% | 21.86 | 586.25 |
| cbd996ad3c1b7dc71fd0e5f5df9087e2 | SP | RJ | beleza_saude | 10 | 5 | 50.00% | 14.75 | 543.02 |
| 88460e8ebdecbfecb5f9601833981930 | PR | MG | informatica_acessorios | 31 | 15 | 48.39% | 8.42 | 4,820.69 |
| d20b021d3efdf267a402c402a48ea64b | SP | RJ | moveis_decoracao | 13 | 6 | 46.15% | 24.40 | 706.47 |
| 54965bbe3e4f07ae045b90b0b8541f52 | PR | MG | cama_mesa_banho | 11 | 5 | 45.45% | 29.20 | 1,953.25 |
| 7aa4334be125fcdd2ba64b3180029f14 | SP | RJ | brinquedos | 21 | 9 | 42.86% | 14.89 | 2,078.98 |
| 06a2c3af7b3aee5d69171b0e14f0ee87 | MA | MA | beleza_saude | 14 | 6 | 42.86% | 2.50 | 1,359.84 |

## Prioritization logic

High-priority operational review should combine:

1. **Order volume:** enough orders to justify investigation.
2. **Late rate:** high share of orders missing delivery promise.
3. **Late-order severity:** high average days late among late orders.
4. **Commercial exposure:** meaningful gross item value.
5. **Proposed owner path:** likely next team where data supports ownership; unresolved category or seller-mapping gaps need data-quality review first.

## Recommended investigation shortlist

| Segment | Why it matters | Suggested owner path |
|---|---|---|
| Seller `88460e8e...` / PR → MG / informatica_acessorios | Highest volume among top rows (`31` orders), high late rate (`48.39%`), and meaningful gross item value (`4,820.69`) | Seller management + regional lane review |
| Seller `2c9e548b...` / SP → RJ / papelaria | High late rate (`57.14%`) and severe late-order delay (`22.75` days) | Seller management + carrier/lane review |
| Seller `54965bbe...` / PR → MG / cama_mesa_banho | Very high late-order severity (`29.20` days) despite small volume | Root-cause sample review before policy action |
| Seller `06a2c3af...` / MA → ES / beleza_saude | High late rate (`53.85%`) and severe delay (`12.83` days), with same seller appearing in another top row | Seller-level fulfillment review |

## Business interpretation

- **Seller/category/region prioritization:** Risk is concentrated enough to build an investigation queue rather than treating delivery performance as one blended average.
- **Sample-size caution:** Rows near the 10-order threshold are useful signals, but they should trigger investigation, not automatic seller penalties or category policy changes.
- **Owner accountability:** Including `seller_id` makes seller-management follow-up possible; state-only grouping is too broad for action.
- **Inventory proxy honesty:** These segments may hint at fulfillment strain or demand-planning pressure, but Olist lacks direct inventory fields. Do not label them as confirmed inventory outcome cases.

## Recommended next actions

1. Raise minimum-volume thresholds before executive reporting; keep small rows as exception-review candidates.
2. Compare top-risk lanes against fulfillment lead time and carrier transit time once stage-level null handling is finalized.
3. Normalize category names with the translation file before dashboard polish.
4. Use these rows to guide deeper SQL/notebook analysis, not as final operational policy.
