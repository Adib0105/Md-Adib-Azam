# 39. Power BI Executive Profit Scorecard

Tool: **Power BI** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

Which region-category combinations drive profit?

## Run and reproduce

From the collection root:

```bash
python 39-power-bi-executive-profit-scorecard/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py) · [SQL](analysis.sql) · [Desktop build guide](BUILD.md)

## Method

SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 12. First five records:

```csv
region,category,sales,profit,orders
West,Office Supplies,220853.249,52609.849,1169
East,Technology,264973.981,47462.0351,443
West,Technology,251991.832,44303.6496,490
East,Office Supplies,205516.055,41014.5791,1074
Central,Technology,170416.312,33697.432,356
```

Desktop implementation pack: calculations, precise target output and build instructions are provided. Native PBIX/TWBX creation and desktop execution are NOT verified.

## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
