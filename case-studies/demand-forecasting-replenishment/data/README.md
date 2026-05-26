# Favorita Data Setup

This case uses the public Corporación Favorita Grocery Sales Forecasting dataset from Kaggle.

Download locally from:

<https://www.kaggle.com/c/favorita-grocery-sales-forecasting/data>

Place source CSV files in:

```text
case-studies/demand-forecasting-replenishment/data/raw/
```

Expected core files for the proof slice:

```text
train.csv
items.csv
stores.csv
```

Optional context files, if available:

```text
transactions.csv
holidays_events.csv
oil.csv
```

## Public data policy

Raw dataset files stay local only. Kaggle competition terms apply; do not redistribute source CSVs. They are ignored by git and must not be copied into `docs/`.

Published dashboard data must be aggregate JSON only:

```text
docs/demand-forecasting-replenishment/assets/data/
```

The pipeline exits with setup guidance when raw files are missing. This keeps the public portfolio safe while leaving the analysis reproducible for local review.
