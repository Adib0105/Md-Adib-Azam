# 50. Tableau Order Size Distribution

Tool: **Tableau** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

How does order size relate to order-level profit by quantity band?

## Run and reproduce

From the collection root:

```bash
python 50-tableau-order-size-distribution/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py) · [SQL](analysis.sql) · [Desktop build guide](BUILD.md)

## Method

SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 4. First five records:

```csv
size_band,orders,average_order_sales,profit
01: 1-5 units,2413,183.515,55348.4284
02: 6-10 units,1457,449.8685,70432.1972
03: 11-20 units,904,908.6935,135914.3393
04: 21+ units,235,1606.2211,24702.0568
```

Desktop implementation pack: calculations, precise target output and build instructions are provided. Native PBIX/TWBX creation and desktop execution are NOT verified.

## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
