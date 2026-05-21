---
title: 'SQL and Notebook Foundation for Olist Delivery Risk Case Study'
type: 'feature'
created: '2026-05-21 20:44:01'
status: 'done'
baseline_commit: '34eb5073879b259fc84c49b01787e2dcd7506d25'
context:
  - '/a0/usr/projects/ba/.a0proj/_bmad-output/planning-artifacts/product-brief-ba-2026-05-14.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The portfolio case study has BA framing and placeholder artifacts, but no SQL or notebook foundation proving real data analysis capability. Hiring reviewers need to see reproducible Olist data loading, schema understanding, core KPI logic, and first analysis outputs for delivery SLA and inventory-risk proxy work.

**Approach:** Add a lightweight, reviewable data-analysis foundation under `case-studies/inventory-stockout-overstock-analysis/` with SQL scripts, Python notebook/script starter, data folder conventions, and documentation. Focus on reproducible setup and first KPI-ready analytical tables, not final dashboard polish.

## Boundaries & Constraints

**Always:** Use the existing case-study folder. Keep raw public dataset files out of git. Treat inventory analysis as proxy logic because Olist lacks stock-on-hand and replenishment fields. Preserve business framing: delivery SLA risk, fulfillment delay, seller/category/geography risk, customer review impact. Make outputs understandable to both BA and DA reviewers.

**Ask First:** Before downloading large dataset files into repo, committing generated outputs, changing the case-study title, adding heavy dependencies, or switching from notebook/script foundation to dashboard work.

**Never:** Do not fake direct stockout or overstock metrics from missing inventory fields. Do not build a generic sales dashboard. Do not require credentials or paid services. Do not commit raw Kaggle data, virtual environments, notebook checkpoints, or large generated files.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Fresh repo setup | No Olist CSVs available locally | Documentation explains exact dataset placement and scripts fail with clear missing-file guidance | Print expected filenames and target folder |
| Local data available | Olist CSVs placed under ignored raw-data folder | SQL/notebook foundation can load or reference core tables and derive order delivery metrics | Validate required columns before analysis |
| Missing optional review data | `order_reviews` unavailable | Delivery metrics still load; review-impact section skipped or marked unavailable | Clear warning, no crash |
| Inventory proxy request | No stock-on-hand fields exist | Proxy metrics use demand velocity/category/seller/order patterns and label limitations | Assumptions documented in artifacts |

</frozen-after-approval>

## Code Map

- `README.md` -- root portfolio overview; should keep case-study promise aligned with new SQL/notebook foundation.
- `case-studies/inventory-stockout-overstock-analysis/README.md` -- case-study entry point; needs setup, data placement, SQL/notebook run order.
- `case-studies/inventory-stockout-overstock-analysis/sql/` -- currently empty; target for schema/KPI/query scripts.
- `case-studies/inventory-stockout-overstock-analysis/notebooks/` -- currently empty; target for reproducible analysis starter notebook or paired Python script.
- `case-studies/inventory-stockout-overstock-analysis/data/` -- currently empty; target for ignored raw/interim/processed folder conventions and keep files.
- `case-studies/inventory-stockout-overstock-analysis/artifacts/*.md` -- placeholder BA artifacts; update only if needed to document KPI definitions and inventory proxy assumptions.
- `.gitignore` -- already ignores `.a0proj/` and venv; needs dataset/output ignore rules if data folders are added.

## Tasks & Acceptance

**Execution:**
- [x] `.gitignore` -- add Olist raw data, processed outputs, and notebook checkpoint ignore rules -- prevent accidental dataset or generated-file commits.
- [x] `case-studies/inventory-stockout-overstock-analysis/data/README.md` -- document expected Olist CSV filenames, download source, and raw/interim/processed folder policy -- make data setup reproducible without committing data.
- [x] `case-studies/inventory-stockout-overstock-analysis/data/raw/.gitkeep`, `data/interim/.gitkeep`, `data/processed/.gitkeep` -- create folder scaffold -- preserve structure in git.
- [x] `case-studies/inventory-stockout-overstock-analysis/sql/00_schema_overview.sql` -- add table inventory and key join comments for Olist orders/items/customers/sellers/products/reviews/payments -- show schema understanding.
- [x] `case-studies/inventory-stockout-overstock-analysis/sql/01_delivery_sla_metrics.sql` -- add delivery SLA KPI query patterns using order timestamps and estimated delivery date -- foundation for late delivery analysis.
- [x] `case-studies/inventory-stockout-overstock-analysis/sql/02_seller_category_region_risk.sql` -- add seller/category/geography aggregation patterns -- foundation for prioritization.
- [x] `case-studies/inventory-stockout-overstock-analysis/sql/03_inventory_proxy_metrics.sql` -- add demand velocity and risk-proxy query patterns with limitations comments -- avoid false inventory certainty.
- [x] `case-studies/inventory-stockout-overstock-analysis/notebooks/01_olist_delivery_risk_foundation.py` -- add notebook-style Python script that checks files, loads core CSVs with pandas, validates columns, creates delivery KPI columns, and prints first summary tables -- runnable foundation even without `.ipynb` tooling.
- [x] `case-studies/inventory-stockout-overstock-analysis/README.md` -- update run order and portfolio reviewer guide -- help hiring reviewer understand what to inspect first.
- [x] `case-studies/inventory-stockout-overstock-analysis/artifacts/kpi-tree.md` and `assumptions.md` -- replace placeholders with delivery SLA and inventory proxy definitions -- align BA artifacts with analysis foundation.

**Acceptance Criteria:**
- Given repo has no raw Olist CSV files, when user reads `data/README.md` and runs the Python foundation script, then expected filenames and placement are clear and missing-data failure is understandable.
- Given Olist CSVs are placed in `case-studies/inventory-stockout-overstock-analysis/data/raw/`, when Python foundation script runs, then it loads required tables, validates required columns, creates delivery timing metrics, and prints summary outputs without requiring paid services.
- Given reviewer opens SQL folder, when they inspect scripts in numeric order, then they see schema joins, delivery SLA metrics, seller/category/region risk, and inventory proxy logic with limitation comments.
- Given reviewer opens case-study README, when they scan first screen, then they understand this is an ecommerce fulfillment/delivery SLA risk case, not generic sales dashboard.
- Given inventory proxy metrics are documented, when reviewer checks assumptions, then they see direct stockout/overstock is not claimed because Olist lacks stock-on-hand data.

## Spec Change Log

- 2026-05-21 review patch: fixed documented pandas setup path, pandas import scope for downstream functions, data-present script path verification, avg_days_late no-late edge case, nonnumeric review_score handling, robust delay bins, and SQL COALESCE for price/freight. Frozen intent unchanged.

## Design Notes

Use SQL as portfolio communication even if no database engine is committed. Prefer ANSI-style CTEs and clear comments; note that scripts can be adapted to DuckDB/Postgres/BigQuery. Use Python script as notebook-compatible foundation: cells separated by `# %%`, pandas only unless already available, and explicit path constants. This keeps implementation lightweight while giving GitHub reviewers visible code without requiring Jupyter rendering.

## Verification

**Commands:**
- `python case-studies/inventory-stockout-overstock-analysis/notebooks/01_olist_delivery_risk_foundation.py` -- expected: clear missing-file guidance if data absent, or summary tables if data present.
- `find case-studies/inventory-stockout-overstock-analysis -maxdepth 3 -type f | sort` -- expected: data README, `.gitkeep` files, SQL scripts, Python foundation script, updated README/artifacts present.
- `git status --short` -- expected: only intended portfolio files changed; no raw CSVs or generated large files tracked.


**Review Patch Verification (2026-05-21):**
- `python -m pip install pandas` -- installed `pandas 3.0.3` and `numpy 2.4.6` locally after approval.
- `python -m py_compile case-studies/inventory-stockout-overstock-analysis/notebooks/01_olist_delivery_risk_foundation.py` -- pass.
- `python case-studies/inventory-stockout-overstock-analysis/notebooks/01_olist_delivery_risk_foundation.py` with no raw CSVs -- pass; prints missing-file guidance.
- Same script with minimal required CSVs plus nonnumeric review score -- pass; prints SLA summary, delay bands, COALESCE-safe gross values, and drops nonnumeric review score with warning.

## Suggested Review Order

**Analysis entry point**

- Runnable foundation shows data checks, KPI creation, and reviewer outputs.
  [`01_olist_delivery_risk_foundation.py:1`](../../../case-studies/inventory-stockout-overstock-analysis/notebooks/01_olist_delivery_risk_foundation.py#L1)

- Missing-data path explains setup without crashing when CSVs are absent.
  [`01_olist_delivery_risk_foundation.py:57`](../../../case-studies/inventory-stockout-overstock-analysis/notebooks/01_olist_delivery_risk_foundation.py#L57)

**Delivery SLA logic**

- Delivery metrics convert timestamps into SLA, lead-time, and lateness signals.
  [`01_olist_delivery_risk_foundation.py:113`](../../../case-studies/inventory-stockout-overstock-analysis/notebooks/01_olist_delivery_risk_foundation.py#L113)

- SQL defines delivery SLA KPIs for warehouse adaptation.
  [`01_delivery_sla_metrics.sql:1`](../../../case-studies/inventory-stockout-overstock-analysis/sql/01_delivery_sla_metrics.sql#L1)

**Risk segmentation and inventory proxy**

- Segment summaries prioritize seller, region, and category delivery risk.
  [`01_olist_delivery_risk_foundation.py:180`](../../../case-studies/inventory-stockout-overstock-analysis/notebooks/01_olist_delivery_risk_foundation.py#L180)

- SQL aggregation frames operational prioritization by seller/category/geography.
  [`02_seller_category_region_risk.sql:1`](../../../case-studies/inventory-stockout-overstock-analysis/sql/02_seller_category_region_risk.sql#L1)

- Inventory proxy SQL labels demand signals without claiming stock certainty.
  [`03_inventory_proxy_metrics.sql:1`](../../../case-studies/inventory-stockout-overstock-analysis/sql/03_inventory_proxy_metrics.sql#L1)

**Reviewer documentation**

- Case README leads with delivery-risk framing, not generic dashboard framing.
  [`README.md:1`](../../../case-studies/inventory-stockout-overstock-analysis/README.md#L1)

- KPI tree maps formulas to business interpretation and action paths.
  [`kpi-tree.md:1`](../../../case-studies/inventory-stockout-overstock-analysis/artifacts/kpi-tree.md#L1)

- Assumptions document protects inventory proxy limits explicitly.
  [`assumptions.md:1`](../../../case-studies/inventory-stockout-overstock-analysis/artifacts/assumptions.md#L1)

**Data and guardrails**

- Data README documents exact filenames and local-only folder policy.
  [`README.md:1`](../../../case-studies/inventory-stockout-overstock-analysis/data/README.md#L1)

- Gitignore blocks raw data, generated outputs, and notebook checkpoints.
  [`.gitignore:13`](../../../.gitignore#L13)


## Suggested Review Order — Review Patch

**Runtime dependency and import scope**

- pandas install path is explicit for local reviewer setup.
  [`README.md:38`](../../../case-studies/inventory-stockout-overstock-analysis/README.md#L38)

- data README documents full pandas setup and run path.
  [`README.md:28`](../../../case-studies/inventory-stockout-overstock-analysis/data/README.md#L28)

- pandas stays available after lazy import for downstream functions.
  [`01_olist_delivery_risk_foundation.py:90`](../../../case-studies/inventory-stockout-overstock-analysis/notebooks/01_olist_delivery_risk_foundation.py#L90)

**Python edge cases**

- delay bins use infinities so extreme lateness remains categorized.
  [`01_olist_delivery_risk_foundation.py:171`](../../../case-studies/inventory-stockout-overstock-analysis/notebooks/01_olist_delivery_risk_foundation.py#L171)

- no-late orders return `0.0`, not `NaN`.
  [`01_olist_delivery_risk_foundation.py:193`](../../../case-studies/inventory-stockout-overstock-analysis/notebooks/01_olist_delivery_risk_foundation.py#L193)

- nonnumeric review scores are dropped with warning before aggregation.
  [`01_olist_delivery_risk_foundation.py:238`](../../../case-studies/inventory-stockout-overstock-analysis/notebooks/01_olist_delivery_risk_foundation.py#L238)

**SQL null-money handling**

- seller/category gross value handles null price and freight safely.
  [`02_seller_category_region_risk.sql:15`](../../../case-studies/inventory-stockout-overstock-analysis/sql/02_seller_category_region_risk.sql#L15)

- inventory proxy revenue metrics coalesce nullable money fields.
  [`03_inventory_proxy_metrics.sql:13`](../../../case-studies/inventory-stockout-overstock-analysis/sql/03_inventory_proxy_metrics.sql#L13)

**Verification trail**

- spec records review patch verification commands and outcomes.
  [`spec-sql-notebook-foundation.md:85`](spec-sql-notebook-foundation.md#L85)
