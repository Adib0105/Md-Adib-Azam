# 16. Product Sales Concentration

Tool: **SQL** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

How concentrated is revenue across products?

## Run and reproduce

From the collection root:

```bash
python 16-product-sales-concentration/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py) · [SQL](analysis.sql)

## Method

SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 1,862. First five records:

```csv
product_id,sales,cumulative_share
TEC-CO-10004722,61599.824,0.0268
OFF-BI-10003527,27453.384,0.0388
TEC-MA-10002412,22638.48,0.0486
FUR-CH-10002024,21870.576,0.0581
OFF-BI-10001359,19823.479,0.0668
```


## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
