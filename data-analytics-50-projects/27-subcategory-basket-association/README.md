# 27. Subcategory Basket Association

Tool: **Python** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

Which subcategory pairs co-occur in at least 20 orders, and with what lift?

## Run and reproduce

From the collection root:

```bash
python 27-subcategory-basket-association/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py)

## Method

Implementation: ../engine.py, function python_analysis, branch `basket`. This shared implementation is versioned and auditable.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 96. First five records:

```csv
item_a,item_b,orders_together,support,confidence_a_to_b,lift
Appliances,Supplies,24,0.0048,0.0532,1.4254
Furnishings,Machines,27,0.0054,0.0308,1.3769
Accessories,Machines,22,0.0044,0.0306,1.3703
Bookcases,Labels,21,0.0042,0.0938,1.3572
Copiers,Paper,20,0.004,0.2941,1.237
```


## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
