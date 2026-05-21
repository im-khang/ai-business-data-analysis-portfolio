# 📦 Data Setup: Olist Brazilian E-Commerce Dataset

This case study uses the public **Olist Brazilian E-Commerce Public Dataset** from Kaggle:

<https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce>

Raw dataset files are intentionally **not committed**. Download the dataset locally and place the CSV files in:

```text
case-studies/inventory-stockout-overstock-analysis/data/raw/
```

## Expected CSV Files

Required for the foundation script:

- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_customers_dataset.csv`
- `olist_sellers_dataset.csv`
- `olist_products_dataset.csv`

Optional but recommended:

- `olist_order_reviews_dataset.csv`
- `olist_order_payments_dataset.csv`
- `product_category_name_translation.csv`

## Python Environment

The foundation script needs pandas after CSV files are present. From repo root, use one local setup path:

```bash
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip pandas
python case-studies/inventory-stockout-overstock-analysis/notebooks/01_olist_delivery_risk_foundation.py
```

If data is absent, the script still prints missing-file guidance before importing pandas.

## Folder Policy

```text
data/raw/       # local downloaded Kaggle CSVs; ignored by git
data/interim/   # temporary joins or exploratory outputs; ignored by git
data/processed/ # cleaned/exported analysis tables; ignored by git
```

Keep `.gitkeep` files only so folder structure remains visible in GitHub.

## Missing-Data Behavior

If raw CSV files are absent, run script anyway:

```bash
python case-studies/inventory-stockout-overstock-analysis/notebooks/01_olist_delivery_risk_foundation.py
```

Expected behavior: script prints missing filenames, target folder, and download source. No paid service or credential required.
