# 42. Power BI Discount Exposure

Tool: **Power BI** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

Which region-discount combinations show loss exposure?

## Run and reproduce

From the collection root:

```bash
python 42-power-bi-discount-exposure/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py) · [SQL](analysis.sql) · [Desktop build guide](BUILD.md)

## Method

SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 15. First five records:

```csv
region,discount_band,lines,sales,profit,loss_line_rate
Central,0–20%,852,128955.152,15973.1962,0.135
Central,20–40%,187,98974.9728,-11598.8353,0.9091
Central,Above 40%,456,30159.126,-40793.4391,1.0
Central,No discount,828,243150.64,76125.4407,0.0
East,0–20%,938,191168.303,28233.8412,0.1279
```

Desktop implementation pack: calculations, precise target output and build instructions are provided. Native PBIX/TWBX creation and desktop execution are NOT verified.

## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
