# 38. Loss Order Wilson Interval

Tool: **Statistics** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

What is the loss-order proportion and Wilson confidence interval?

## Run and reproduce

From the collection root:

```bash
python 38-loss-order-wilson-interval/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py)

## Method

Implementation: ../engine.py, function statistics_analysis, branch `wilson`. This shared implementation is versioned and auditable.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 1. First five records:

```csv
n_orders,loss_orders,loss_rate,lower_95,upper_95
5009,1022,0.204,0.1931,0.2154
```

Exploratory inference only. Historical sample, repeated customers, skew and non-random assignment limit generalization. See the metric contract for exact assumptions.

## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
