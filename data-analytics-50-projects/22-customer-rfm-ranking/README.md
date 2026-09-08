# 22. Customer RFM Ranking

Tool: **Python** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

Which customers score highly on recency, frequency and observed monetary value?

## Run and reproduce

From the collection root:

```bash
python 22-customer-rfm-ranking/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py)

## Method

Implementation: ../engine.py, function python_analysis, branch `rfm`. This shared implementation is versioned and auditable.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 793. First five records:

```csv
customer_id,frequency,monetary,recency_days,recency_score,frequency_score,monetary_score,rfm_sum
SE-20110,11,12209.438,10,5,5,5,15
JL-15835,11,9799.923,22,5,5,5,15
PK-19075,12,8646.934,10,5,5,5,15
HM-14860,10,8236.7648,3,5,5,5,15
LC-16885,12,7663.126,17,5,5,5,15
```


## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
