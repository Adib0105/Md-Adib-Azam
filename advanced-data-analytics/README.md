# Advanced Data Analytics Portfolio — 20 Real-World Projects

An industry-style analytics collection by **Md Adib Azam**. Every project contains a reproducible synthetic data generator, a real analytical or machine-learning pipeline, business metrics, and an automatically generated decision brief.

## What makes this collection advanced

- Time-aware validation, cost-sensitive ranking and capacity-based evaluation
- Forecasting, anomaly detection, experimentation, NLP, recommender systems and graph analytics
- Calibration, fairness, subgroup error and drift checks for responsible deployment
- Deterministic synthetic datasets that run without downloading private or unstable data
- Automated smoke tests and GitHub Actions CI

## Project index

| # | Project | Business outcome | Methods |
|---:|---|---|---|
| 01 | [Retail Demand Forecasting](projects/01-retail-demand-forecasting/) | SKU-level time-series forecasting with lag, rolling, price and promotion signals. | Gradient boosting, temporal validation, WAPE, peak-demand planning |
| 02 | [Customer Churn & Retention](projects/02-customer-churn-survival/) | Ranks subscribers by churn risk and quantifies the value of a targeted retention campaign. | Boosted classification, ROC-AUC, lift@10%, value-at-risk |
| 03 | [Credit Risk Scorecard](projects/03-credit-risk-scorecard/) | Produces calibrated probability-of-default estimates and portfolio expected loss. | Logistic scorecard, KS statistic, Brier score, PD bands |
| 04 | [Payment Fraud Anomaly Detection](projects/04-fraud-anomaly-detection/) | Detects rare suspicious payments without using labels during model training. | Isolation Forest, precision-recall, recall@investigation-capacity |
| 05 | [Inventory & Service-Level Optimizer](projects/05-inventory-optimization/) | Optimizes reorder points using demand uncertainty, lead time and holding cost. | Monte Carlo simulation, safety stock, stockout risk, cost trade-offs |
| 06 | [Multi-Touch Marketing Attribution](projects/06-marketing-attribution/) | Measures the incremental contribution of channels across customer journeys. | Path analytics, removal effects, assisted conversions, budget guidance |
| 07 | [Experiment Analysis with CUPED](projects/07-ab-testing-cuped/) | Estimates product-test lift with variance reduction, confidence intervals and power diagnostics. | CUPED, Welch test, bootstrap CI, practical significance |
| 08 | [Customer Segmentation & CLV](projects/08-customer-segmentation-clv/) | Builds behavior-based segments and prioritizes customers by predicted lifetime value. | RFM, K-Means, silhouette score, CLV economics |
| 09 | [Hospital Readmission Risk](projects/09-healthcare-readmission/) | Predicts 30-day readmission and audits subgroup performance for deployment safety. | Gradient boosting, calibration, recall@capacity, subgroup gap |
| 10 | [HR Attrition & Fairness Audit](projects/10-hr-attrition-fairness/) | Predicts employee attrition while reporting demographic parity and opportunity gaps. | Explainable logistic model, ROC-AUC, fairness diagnostics |
| 11 | [Geospatial Demand Hotspots](projects/11-geospatial-demand-hotspots/) | Finds stable ride-demand hotspots and quantifies spatial coverage and noise. | DBSCAN, haversine-ready coordinates, hotspot prioritization |
| 12 | [Energy Load Forecasting](projects/12-energy-load-forecasting/) | Forecasts hourly electricity demand and validates peak-load and interval performance. | Cyclical features, boosting, MAPE, prediction-interval coverage |
| 13 | [Personalized Recommender System](projects/13-recommender-system/) | Learns latent user-item preferences and evaluates top-N recommendations offline. | Matrix factorization, precision@5, recall@5, catalog coverage |
| 14 | [NLP Voice-of-Customer Intelligence](projects/14-nlp-sentiment-intelligence/) | Classifies feedback sentiment and detects vocabulary drift in new reviews. | TF-IDF, logistic regression, macro-F1, drift monitoring |
| 15 | [Social Network Influence Analytics](projects/15-social-network-influence/) | Ranks influential accounts and measures concentration and community structure. | PageRank from scratch, graph components, influence concentration |
| 16 | [Portfolio Risk & Stress Testing](projects/16-market-risk-stress-testing/) | Estimates VaR/CVaR and compares historical, Monte Carlo and stressed losses. | Correlated simulation, VaR, expected shortfall, scenario analysis |
| 17 | [Telecom Network KPI Anomalies](projects/17-telecom-kpi-anomalies/) | Detects degraded cell towers from multivariate operational KPIs. | Isolation Forest, capacity-aware recall, cell prioritization |
| 18 | [Airline Delay Root-Cause Analytics](projects/18-airline-delay-root-cause/) | Forecasts delay minutes and ranks operational drivers with permutation importance. | Boosted regression, MAE, severe-delay AUC, driver ranking |
| 19 | [Real Estate Price Explainability](projects/19-real-estate-explainability/) | Predicts property prices and audits error by market segment. | Nonlinear regression, permutation importance, segment error audit |
| 20 | [Predictive Maintenance Economics](projects/20-predictive-maintenance/) | Prioritizes machines likely to fail and estimates avoidable maintenance cost. | Random forest, PR-AUC, recall@10%, cost-benefit simulation |

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r advanced-data-analytics/requirements.txt
python advanced-data-analytics/run_all.py
```

On Windows use `.venv\Scripts\activate`. Individual projects can be run with `python advanced-data-analytics/projects/<project>/app.py`.

## Outputs

Each run creates `artifacts/<project>/metrics.json` and `decision_brief.md`. The data is generated locally with fixed random seeds, making every result reproducible.

## Validation

```bash
pytest advanced-data-analytics/tests -q
```

> Portfolio note: the datasets are realistic simulations designed to demonstrate end-to-end analytical capability. They are not presented as confidential company data.
