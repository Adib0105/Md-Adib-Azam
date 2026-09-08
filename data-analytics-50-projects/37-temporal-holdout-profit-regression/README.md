# 37. Temporal Holdout Profit Regression

Tool: **Statistics** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

How does a sales-only regression predict order profit on a later temporal holdout?

## Run and reproduce

From the collection root:

```bash
python 37-temporal-holdout-profit-regression/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py)

## Method

Implementation: ../engine.py, function statistics_analysis, branch `regression`. This shared implementation is versioned and auditable.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 1. First five records:

```csv
train_orders,test_orders,slope,intercept,train_r_squared,test_mae,test_rmse,test_r_squared
4007,1002,0.1751,-22.1334,0.2401,99.5521,308.5853,0.2166
```

Exploratory inference only. Historical sample, repeated customers, skew and non-random assignment limit generalization. See the metric contract for exact assumptions.

## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
