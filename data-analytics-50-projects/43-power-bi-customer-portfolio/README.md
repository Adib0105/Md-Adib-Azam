# 43. Power BI Customer Portfolio

Tool: **Power BI** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

Which region-segment combinations create customer value?

## Run and reproduce

From the collection root:

```bash
python 43-power-bi-customer-portfolio/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py) · [SQL](analysis.sql) · [Desktop build guide](BUILD.md)

## Method

SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 12. First five records:

```csv
region,segment,customers,sales,profit
West,Consumer,358,362880.773,57450.604
East,Consumer,344,350908.167,41190.9843
Central,Consumer,328,252031.434,8564.0481
West,Corporate,204,225855.2745,34437.4299
East,Corporate,206,200409.347,23622.5789
```

Desktop implementation pack: calculations, precise target output and build instructions are provided. Native PBIX/TWBX creation and desktop execution are NOT verified.

## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
