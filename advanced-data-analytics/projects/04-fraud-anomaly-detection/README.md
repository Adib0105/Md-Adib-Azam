# 04. Payment Fraud Anomaly Detection

## Business problem

Detects rare suspicious payments without using labels during model training.

## Analytics approach

Isolation Forest, precision-recall, recall@investigation-capacity. The pipeline generates a deterministic, realistic dataset, trains or calculates the analytical model, evaluates decision-focused KPIs, and writes a machine-readable metrics file plus a management brief.

## Run

```bash
python advanced-data-analytics/projects/04-fraud-anomaly-detection/app.py
```

## Deliverables

- Reproducible data simulation and analytical pipeline
- Model or decision metrics in `metrics.json`
- Actionable recommendations in `decision_brief.md`
- Smoke-tested execution through the collection CI
