# 41. Power BI Product Profit Matrix

Tool: **Power BI** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

Where does product revenue coexist with negative profitability?

## Run and reproduce

From the collection root:

```bash
python 41-power-bi-product-profit-matrix/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py) · [SQL](analysis.sql) · [Desktop build guide](BUILD.md)

## Method

SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 17. First five records:

```csv
category,sub_category,sales,profit,margin
Furniture,Tables,206965.532,-17725.4811,-0.0856
Furniture,Bookcases,114879.9963,-3472.556,-0.0302
Office Supplies,Supplies,46673.538,-1189.0995,-0.0255
Office Supplies,Fasteners,3024.28,949.5182,0.314
Technology,Machines,189238.631,3384.7569,0.0179
```

Desktop implementation pack: calculations, precise target output and build instructions are provided. Native PBIX/TWBX creation and desktop execution are NOT verified.

## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
