# 48. Tableau Category Share Story

Tool: **Tableau** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

How does category sales mix change across years?

## Run and reproduce

From the collection root:

```bash
python 48-tableau-category-share-story/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py) · [SQL](analysis.sql) · [Desktop build guide](BUILD.md)

## Method

SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 12. First five records:

```csv
order_year,category,sales,annual_share
2014,Furniture,157192.8531,0.3246
2014,Office Supplies,151776.412,0.3134
2014,Technology,175278.233,0.362
2015,Furniture,170518.237,0.3624
2015,Office Supplies,137233.463,0.2917
```

Desktop implementation pack: calculations, precise target output and build instructions are provided. Native PBIX/TWBX creation and desktop execution are NOT verified.

## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
