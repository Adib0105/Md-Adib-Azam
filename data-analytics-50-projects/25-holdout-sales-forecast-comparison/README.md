# 25. Holdout Sales Forecast Comparison

Tool: **Python** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

Does seasonal naive beat a three-month mean on the last 12 months?

## Run and reproduce

From the collection root:

```bash
python 25-holdout-sales-forecast-comparison/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py)

## Method

Implementation: ../engine.py, function python_analysis, branch `forecast`. This shared implementation is versioned and auditable.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 12. First five records:

```csv
month,actual_sales,seasonal_naive,three_month_mean,seasonal_abs_error,mean_abs_error
2017-01,43971.374,18542.491,78699.5846,25428.883,34728.2106
2017-02,20301.1334,22978.815,78699.5846,2677.6816,58398.4512
2017-03,58872.3528,51715.875,78699.5846,7156.4778,19827.2318
2017-04,36521.5361,38750.039,78699.5846,2228.5029,42178.0485
2017-05,44261.1102,56987.728,78699.5846,12726.6178,34438.4744
```

Seasonal-naive holdout MAE: 15,467.89; three-month-mean MAE: 26,605.82. No model tuning on the test period.

## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
