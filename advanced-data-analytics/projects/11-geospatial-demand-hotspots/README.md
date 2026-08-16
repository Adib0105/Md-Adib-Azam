# 11. Geospatial Demand Hotspots

## Business problem

Finds stable ride-demand hotspots and quantifies spatial coverage and noise.

## Analytics approach

DBSCAN, haversine-ready coordinates, hotspot prioritization. The pipeline generates a deterministic, realistic dataset, trains or calculates the analytical model, evaluates decision-focused KPIs, and writes a machine-readable metrics file plus a management brief.

## Run

```bash
python advanced-data-analytics/projects/11-geospatial-demand-hotspots/app.py
```

## Deliverables

- Reproducible data simulation and analytical pipeline
- Model or decision metrics in `metrics.json`
- Actionable recommendations in `decision_brief.md`
- Smoke-tested execution through the collection CI
