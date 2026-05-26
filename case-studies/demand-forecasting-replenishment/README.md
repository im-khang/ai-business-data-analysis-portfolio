# 📦 Demand Forecasting & Replenishment Planner Queue

This case study turns retail demand forecasts into planner-ready replenishment review decisions using the public Corporación Favorita Grocery Sales Forecasting dataset. The primary outcome is a ranked **Planner Exception Queue**, not a forecasting model leaderboard.

## 🎯 Business Question

Which item/store/family combinations need replenishment review first, and what reasons (demand volume, forecast error, bias direction, demand variability, replenishment assumption) justify each exception?

## 🧭 Reviewer Guide

1. [Live dashboard](https://im-khang.github.io/ai-business-data-analysis-portfolio/demand-forecasting-replenishment/) — Overview · Forecast Accuracy · Planner Queue · Assumptions.
2. `dashboard/lib/metrics.py` — tested forecast metric formulas (WAPE, MAE, Bias %, Forecast Score, FVA).
3. `notebooks/01_run_pipeline.py` — controlled Favorita slice → naïve + moving-average baselines → metrics → ABC/XYZ → safety stock + reorder point assumptions → ranked planner queue.
4. `dashboard/export_pages_data.py` — aggregate JSON exporter with size + schema guards.
5. `tests/` — pytest coverage for metric formulas (including zero-demand) and exporter behavior.

## 📦 Data Setup

Raw Favorita CSVs stay local in `data/raw/` and are git-ignored. See `data/README.md` for download steps.

```bash
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip pandas numpy pytest
```

## ▶️ Run Order

From repo root:

```bash
pytest case-studies/demand-forecasting-replenishment/tests/ -q
python case-studies/demand-forecasting-replenishment/notebooks/01_run_pipeline.py
python case-studies/demand-forecasting-replenishment/dashboard/export_pages_data.py
python case-studies/demand-forecasting-replenishment/dashboard/export_pages_data.py --check
python -m http.server -d docs 8000
# open http://localhost:8000/demand-forecasting-replenishment/
```

With no raw data present, the pipeline prints setup guidance and exits 0 without touching public dashboard assets.

## 📊 What the Pipeline Produces

- Naïve and moving-average baseline forecasts on a controlled SKU/store/family slice.
- WAPE, MAE, Bias %, Forecast Score, and FVA per item/store/family.
- ABC segmentation by demand importance and XYZ segmentation by demand variability.
- Safety stock and reorder point estimates labeled as planning assumptions.
- Planner Exception Queue ranked by demand volume, |bias|, error, and variability — with reason codes (`high_volume`, `under_forecast_bias`, `over_forecast_bias`, `high_error`, `volatile_demand`, `replenishment_risk`) and recommended review actions.
- Aggregate dashboard JSON: `kpis.json`, `forecast_accuracy.json`, `planner_queue.json`, `segments.json`, `assumptions.json`, `build_metadata.json` (each ≤ 500 KB, total ≤ 2 MB).

## ⚠️ Caveats

- Public Favorita data does not include true stock on hand, supplier lead-time history, or open purchase orders.
- Safety stock and reorder point outputs are planning decision support, not production order instructions.
- Planner queue rows are review candidates, not automatic purchase actions or proof of stockout/overstock.
- Bias direction is shown beside accuracy because under-forecast and over-forecast create different planning risks. MAPE is intentionally not the primary metric, since zero or low demand can distort it.

## 🛠️ Tools

- Python · pandas · numpy · pytest
- Plotly.js static dashboard on GitHub Pages
- Aggregate JSON only; no backend, login, API server, database, scheduler, or live refresh
