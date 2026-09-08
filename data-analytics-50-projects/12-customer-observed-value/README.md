# 12. Customer Observed Value

Tool: **SQL** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

Which customers generated the most observed revenue, not projected lifetime value?

## Run and reproduce

From the collection root:

```bash
python 12-customer-observed-value/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py) · [SQL](analysis.sql)

## Method

SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 793. First five records:

```csv
customer_id,orders,observed_sales,observed_profit,first_order,last_order
SM-20320,5,25043.05,-1980.7393,2014-03-18,2017-10-12
TC-20980,5,19052.218,8981.3239,2014-11-07,2016-11-26
RB-19360,6,15117.339,6976.0959,2016-04-01,2017-09-25
TA-21385,4,14595.62,4703.7883,2014-09-12,2017-10-22
AB-10105,10,14473.571,5444.8055,2014-12-20,2017-11-19
```


## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
