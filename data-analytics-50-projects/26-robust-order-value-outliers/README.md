# 26. Robust Order Value Outliers

Tool: **Python** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

Which log-order values exceed a robust absolute z-score of 3.5?

## Run and reproduce

From the collection root:

```bash
python 26-robust-order-value-outliers/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py)

## Method

Implementation: ../engine.py, function python_analysis, branch `anomaly`. This shared implementation is versioned and auditable.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 5,009. First five records:

```csv
order_id,sales,profit,robust_z,outlier_flag
CA-2014-145317,23661.228,-1789.7327,2.6495,0
CA-2016-118689,18336.74,8762.3891,2.5155,0
CA-2017-140151,14052.48,6734.472,2.3756,0
CA-2017-127180,13716.458,4597.1657,2.3629,0
CA-2014-139892,10539.896,-1878.7892,2.2245,0
```

Outliers flagged: 0 of 5009 orders at the pre-set |robust z| > 3.5 threshold. All scores are retained; no threshold was lowered to manufacture anomalies.

## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
