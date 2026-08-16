# 17. Telecom Network KPI Anomalies

## Business problem

Detects degraded cell towers from multivariate operational KPIs.

## Analytics approach

Isolation Forest, capacity-aware recall, cell prioritization. The pipeline generates a deterministic, realistic dataset, trains or calculates the analytical model, evaluates decision-focused KPIs, and writes a machine-readable metrics file plus a management brief.

## Run

```bash
python advanced-data-analytics/projects/17-telecom-kpi-anomalies/app.py
```

## Deliverables

- Reproducible data simulation and analytical pipeline
- Model or decision metrics in `metrics.json`
- Actionable recommendations in `decision_brief.md`
- Smoke-tested execution through the collection CI
