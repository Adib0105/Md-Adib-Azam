# 13. Personalized Recommender System

## Business problem

Learns latent user-item preferences and evaluates top-N recommendations offline.

## Analytics approach

Matrix factorization, precision@5, recall@5, catalog coverage. The pipeline generates a deterministic, realistic dataset, trains or calculates the analytical model, evaluates decision-focused KPIs, and writes a machine-readable metrics file plus a management brief.

## Run

```bash
python advanced-data-analytics/projects/13-recommender-system/app.py
```

## Deliverables

- Reproducible data simulation and analytical pipeline
- Model or decision metrics in `metrics.json`
- Actionable recommendations in `decision_brief.md`
- Smoke-tested execution through the collection CI
