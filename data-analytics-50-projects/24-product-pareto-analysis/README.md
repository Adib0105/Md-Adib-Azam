# 24. Product Pareto Analysis

Tool: **Python** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

How many products are needed to account for most sales?

## Run and reproduce

From the collection root:

```bash
python 24-product-pareto-analysis/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py)

## Method

Implementation: ../engine.py, function python_analysis, branch `pareto`. This shared implementation is versioned and auditable.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 1,862. First five records:

```csv
product_id,sales,profit,cumulative_sales_share,product_rank
TEC-CO-10004722,61599.824,25199.928,0.0268,1
OFF-BI-10003527,27453.384,7753.039,0.0388,2
TEC-MA-10002412,22638.48,-1811.0784,0.0486,3
FUR-CH-10002024,21870.576,0.0,0.0581,4
OFF-BI-10001359,19823.479,2233.5051,0.0668,5
```


## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
