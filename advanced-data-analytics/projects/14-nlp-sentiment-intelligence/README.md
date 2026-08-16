# 14. NLP Voice-of-Customer Intelligence

## Business problem

Classifies feedback sentiment and detects vocabulary drift in new reviews.

## Analytics approach

TF-IDF, logistic regression, macro-F1, drift monitoring. The pipeline generates a deterministic, realistic dataset, trains or calculates the analytical model, evaluates decision-focused KPIs, and writes a machine-readable metrics file plus a management brief.

## Run

```bash
python advanced-data-analytics/projects/14-nlp-sentiment-intelligence/app.py
```

## Deliverables

- Reproducible data simulation and analytical pipeline
- Model or decision metrics in `metrics.json`
- Actionable recommendations in `decision_brief.md`
- Smoke-tested execution through the collection CI
