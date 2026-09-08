# 19. Loss Making Order Audit

Tool: **SQL** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

Which orders lose money overall rather than only on individual lines?

## Run and reproduce

From the collection root:

```bash
python 19-loss-making-order-audit/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py) · [SQL](analysis.sql)

## Method

SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 1,022. First five records:

```csv
order_id,customer_id,sales,profit,margin
CA-2016-108196,CS-12505,5016.549,-6892.3748,-1.3739
US-2017-168116,GT-14635,8167.42,-3825.3394,-0.4684
CA-2014-169019,LF-17185,2656.716,-3791.1634,-1.427
CA-2017-134845,SR-20425,2613.309,-3424.3546,-1.3104
US-2017-122714,HG-14965,1889.99,-2929.4845,-1.55
```


## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
