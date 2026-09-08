# 14. State Rank within Region

Tool: **SQL** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

Which states lead sales within each region?

## Run and reproduce

From the collection root:

```bash
python 14-state-rank-within-region/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py) · [SQL](analysis.sql)

## Method

SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 49. First five records:

```csv
region,state,sales,profit,regional_rank
Central,Texas,170188.0458,-25729.3563,1
Central,Illinois,80166.101,-12607.887,2
Central,Michigan,76269.614,24463.1876,3
Central,Indiana,53555.36,18382.9363,4
Central,Wisconsin,32114.61,8401.8004,5
```


## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
