# 04. Monthly Sales and Profit

Tool: **Excel** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

How do sales and profit evolve across all 48 observed months?

## Run and reproduce

From the collection root:

```bash
python 04-monthly-sales-and-profit/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py) · [SQL](analysis.sql) · [Excel workbook](analysis.xlsx)

![Workbook preview](dashboard-preview.png)

## Method

SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 48. First five records:

```csv
dimension,sales,profit,quantity,margin
2014-01,14236.895,2450.1907,284,0.1721
2014-02,4519.892,862.3084,159,0.1908
2014-03,55691.009,498.7299,585,0.009
2014-04,28295.345,3488.8352,536,0.1233
2014-05,23648.287,2738.7096,466,0.1158
```


## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
