# 31. A/B Test Conversion Analysis

**Tool:** Statistics  
**Dataset:** [`../../datasets/marketing_campaigns.csv`](../../datasets/marketing_campaigns.csv)

## Business question

Is the conversion-rate difference statistically meaningful?

## KPIs

- Lift
- Z Score
- P Value
- Confidence Interval

## Workflow

1. Import the linked CSV and confirm data types.
2. Check missing values, duplicate keys and invalid ranges.
3. Create the calculations in `analysis.py`.
4. Validate totals against a simple grouped summary.
5. Present one decision, supported by the KPI output.

## Deliverable

Open [`analysis.py`](analysis.py) for the reproducible analysis. The source data is intentionally small so every result can be checked manually before scaling to a larger dataset.

## Portfolio talking point

This project demonstrates how I translate a business question into clean metrics, a repeatable analysis and a decision-ready output using Statistics.
