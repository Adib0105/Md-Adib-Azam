# 18. Order Level Shipping Intervals

Tool: **SQL** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

What are dispatch intervals by shipping mode when orders are counted once?

## Run and reproduce

From the collection root:

```bash
python 18-order-level-shipping-intervals/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py) · [SQL](analysis.sql)

## Method

SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 4. First five records:

```csv
ship_mode,orders,mean_days,min_days,max_days
Same Day,264,0.0455,0,1
First Class,787,2.1881,1,4
Second Class,964,3.2324,1,5
Standard Class,2994,5.001,3,7
```


## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
