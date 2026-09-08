# 03. Subcategory Loss Exposure

Tool: **Excel** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

Which subcategories have negative profit and concentrated losses?

## Run and reproduce

From the collection root:

```bash
python 03-subcategory-loss-exposure/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py) · [SQL](analysis.sql) · [Excel workbook](analysis.xlsx)

![Workbook preview](dashboard-preview.png)

## Method

SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 17. First five records:

```csv
dimension,sales,profit,quantity,margin
Accessories,167380.318,41936.6357,2976,0.2505
Appliances,107532.161,18138.0054,1729,0.1687
Art,27118.792,6527.787,3000,0.2407
Binders,203412.733,30221.7633,5974,0.1486
Bookcases,114879.9963,-3472.556,868,-0.0302
```


## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
