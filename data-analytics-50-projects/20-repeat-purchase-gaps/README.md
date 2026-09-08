# 20. Repeat Purchase Gaps

Tool: **SQL** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

How long is the interval between consecutive distinct purchase dates?

## Run and reproduce

From the collection root:

```bash
python 20-repeat-purchase-gaps/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py) · [SQL](analysis.sql)

## Method

SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 4,199. First five records:

```csv
customer_id,order_date,prior_date,gap_days
AA-10315,2014-09-15,2014-03-31,168.0
AA-10315,2015-10-04,2014-09-15,384.0
AA-10315,2016-03-03,2015-10-04,151.0
AA-10315,2017-06-29,2016-03-03,483.0
AA-10375,2014-10-24,2014-04-21,186.0
```


## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
