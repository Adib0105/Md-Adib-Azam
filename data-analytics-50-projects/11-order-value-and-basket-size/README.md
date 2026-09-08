# 11. Order Value and Basket Size

Tool: **SQL** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

What is the true average order value after consolidating order lines?

## Run and reproduce

From the collection root:

```bash
python 11-order-value-and-basket-size/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py) · [SQL](analysis.sql)

## Method

SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 5,009. First five records:

```csv
order_id,lines,units,order_sales,order_profit
CA-2014-145317,7,25,23661.228,-1789.7327
CA-2016-118689,5,18,18336.74,8762.3891
CA-2017-140151,3,9,14052.48,6734.472
CA-2017-127180,4,18,13716.458,4597.1657
CA-2014-139892,7,37,10539.896,-1878.7892
```


## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
