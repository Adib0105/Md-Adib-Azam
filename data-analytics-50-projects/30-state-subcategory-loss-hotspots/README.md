# 30. State Subcategory Loss Hotspots

Tool: **Python** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

Which state and subcategory combinations concentrate loss dollars?

## Run and reproduce

From the collection root:

```bash
python 30-state-subcategory-loss-hotspots/analysis.py
```

[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py)

## Method

Implementation: ../engine.py, function python_analysis, branch `loss`. This shared implementation is versioned and auditable.

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: 126. First five records:

```csv
state,sub_category,loss_amount,net_profit,sales,loss_lines
Texas,Binders,14705.0738,-14705.0738,9042.676,153
Ohio,Machines,11770.9447,-11770.9447,8978.238,8
Illinois,Binders,7204.3242,-7204.3242,4538.546,80
Texas,Appliances,6147.2225,-6147.2225,2407.814,47
North Carolina,Machines,5384.8086,-5384.8086,12620.655,4
```


## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
