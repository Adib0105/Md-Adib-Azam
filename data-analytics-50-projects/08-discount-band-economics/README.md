# 08. Discount Band Economics

Tool: **Excel** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

How are discount bands associated with line-level profitability?

## Run and reproduce

From the collection root:

```bash
python 08-discount-band-economics/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py) · [SQL](analysis.sql) · [Excel workbook](analysis.xlsx)

![Workbook preview](dashboard-preview.png)

## Method

SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 4. First five records:

```csv
dimension,sales,profit,quantity,margin
0–20%,846522.2405,100785.4745,14231,0.1191
20–40%,234137.8978,-35817.4655,1740,-0.153
Above 40%,128632.252,-99558.5905,3635,-0.774
No discount,1087908.47,320987.6032,18267,0.2951
```


## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
