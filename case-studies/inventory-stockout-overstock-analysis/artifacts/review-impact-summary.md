# ⭐ Review Impact Summary

## Headline finding

Customer review scores drop sharply for late delivery bands and remain low as delay severity increases. On-time or early orders average **4.29 review score**, while orders late by **4-7 days** average **2.11**, and orders late by **8-14 days** average **1.67**.

This supports the business case that delivery SLA misses are not only logistics metrics; they connect to customer experience and marketplace review outcomes.

## Review score by delay band

| Delay band | Late delivery flag | Orders with review signal | Average review score | Business interpretation |
|---|---|---:|---:|---|
| On time / early | False | 89,443 | 4.29 | Healthy customer experience baseline |
| 1-3 days late | True | 1,852 | 3.29 | Noticeable decline; minor delays still matter |
| 4-7 days late | True | 1,748 | 2.11 | Major customer-experience deterioration |
| 8-14 days late | True | 1,446 | 1.67 | Severe customer-experience damage likely |
| 15+ days late | True | 1,335 | 1.72 | Very poor experience, similar to severe-delay bands |

## Business interpretation

- **Customer review outcome impact:** Review score drops from **4.29** for on-time/early orders to **3.29** for 1-3 day late orders, then near two-star or worse for longer delay bands.
- **Operational priority:** Severe delay bands (`4-7`, `8-14`, `15+`) should receive stronger attention than minor misses because customer impact is much larger.
- **Marketplace management:** Seller/category/region risk prioritization should include review impact, not only late rate or gross item value.
- **Causality caution:** This analysis shows association between late delivery and lower reviews. It does not prove delivery delay is the only cause of low reviews; product quality, seller communication, price, and service issues may also contribute.

## Recommended next actions

1. Add review-impact weighting to seller/category/region prioritization so high-late-rate segments with poor reviews rise in the queue.
2. Compare severe-delay rows against categories and regions to identify customer-facing hot spots.
3. Investigate whether some segments have high late rates but less review damage, which may indicate different customer expectations or communication patterns.
4. Preserve inventory proxy honesty: poor reviews and late delivery can suggest fulfillment stress, but they do not prove stockouts or overstock without inventory snapshots and replenishment data.

## Caveats

Review data is available in the current run, but reviews are customer-submitted outcomes and may reflect multiple drivers beyond delivery speed. This artifact should be used to prioritize investigation and customer-experience risk, not to assign single-cause blame.
