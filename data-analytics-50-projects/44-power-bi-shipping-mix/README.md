# 44. Power BI Shipping Mix

Tool: **Power BI** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

How do order volume and dispatch intervals differ by region and mode?

## Run and reproduce

From the collection root:

```bash
python 44-power-bi-shipping-mix/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py) · [SQL](analysis.sql) · [Desktop build guide](BUILD.md)

## Method

SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 16. First five records:

```csv
region,ship_mode,orders,mean_ship_days
Central,Same Day,62,0.0484
Central,First Class,174,2.2299
Central,Second Class,224,3.3661
Central,Standard Class,715,4.986
East,Same Day,74,0.0
```

Desktop implementation pack: calculations, precise target output and build instructions are provided. Native PBIX/TWBX creation and desktop execution are NOT verified.

## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
