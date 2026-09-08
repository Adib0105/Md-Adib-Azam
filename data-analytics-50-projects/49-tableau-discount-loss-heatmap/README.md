# 49. Tableau Discount Loss Heatmap

Tool: **Tableau** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

Which subcategory-discount cells merit margin investigation?

## Run and reproduce

From the collection root:

```bash
python 49-tableau-discount-loss-heatmap/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py) · [SQL](analysis.sql) · [Desktop build guide](BUILD.md)

## Method

SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 46. First five records:

```csv
sub_category,discount_band,sales,profit,loss_line_rate
Accessories,0–20%,49010.008,6647.3818,0.2993
Accessories,No discount,118370.31,35289.2539,0.0
Appliances,0–20%,26083.437,3583.9105,0.0
Appliances,Above 40%,3382.534,-8629.6412,1.0
Appliances,No discount,78066.19,23183.7361,0.0
```

Desktop implementation pack: calculations, precise target output and build instructions are provided. Native PBIX/TWBX creation and desktop execution are NOT verified.

## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
