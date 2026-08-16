# 08. Customer Segmentation & CLV

## Business problem

Builds behavior-based segments and prioritizes customers by predicted lifetime value.

## Analytics approach

RFM, K-Means, silhouette score, CLV economics. The pipeline generates a deterministic, realistic dataset, trains or calculates the analytical model, evaluates decision-focused KPIs, and writes a machine-readable metrics file plus a management brief.

## Run

```bash
python advanced-data-analytics/projects/08-customer-segmentation-clv/app.py
```

## Deliverables

- Reproducible data simulation and analytical pipeline
- Model or decision metrics in `metrics.json`
- Actionable recommendations in `decision_brief.md`
- Smoke-tested execution through the collection CI
