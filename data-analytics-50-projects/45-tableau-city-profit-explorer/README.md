# 45. Tableau City Profit Explorer

Tool: **Tableau** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

Which city-state combinations generate the strongest and weakest profits?

## Run and reproduce

From the collection root:

```bash
python 45-tableau-city-profit-explorer/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py) · [SQL](analysis.sql) · [Desktop build guide](BUILD.md)

## Method

SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 604. First five records:

```csv
city,state,sales,profit
Philadelphia,Pennsylvania,109077.013,-13837.7674
Houston,Texas,64504.7604,-10153.5485
San Antonio,Texas,21843.528,-7299.0502
Lancaster,Ohio,8202.625,-7149.618
Chicago,Illinois,48539.541,-6654.5688
```

Desktop implementation pack: calculations, precise target output and build instructions are provided. Native PBIX/TWBX creation and desktop execution are NOT verified.

## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
