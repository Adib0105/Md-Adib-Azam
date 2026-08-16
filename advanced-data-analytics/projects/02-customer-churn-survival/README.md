# 02. Customer Churn & Retention

## Business problem

Ranks subscribers by churn risk and quantifies the value of a targeted retention campaign.

## Analytics approach

Boosted classification, ROC-AUC, lift@10%, value-at-risk. The pipeline generates a deterministic, realistic dataset, trains or calculates the analytical model, evaluates decision-focused KPIs, and writes a machine-readable metrics file plus a management brief.

## Run

```bash
python advanced-data-analytics/projects/02-customer-churn-survival/app.py
```

## Deliverables

- Reproducible data simulation and analytical pipeline
- Model or decision metrics in `metrics.json`
- Actionable recommendations in `decision_brief.md`
- Smoke-tested execution through the collection CI
