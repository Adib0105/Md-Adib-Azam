# 50 Data Analytics Projects

[![Projects](https://img.shields.io/badge/Projects-50-7C3AED?style=for-the-badge)](#project-index)
[![Excel](https://img.shields.io/badge/Excel-10-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)](#project-index)
[![SQL](https://img.shields.io/badge/SQL-10-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](#project-index)
[![Python](https://img.shields.io/badge/Python-10-3776AB?style=for-the-badge&logo=python&logoColor=white)](#project-index)
[![Statistics](https://img.shields.io/badge/Statistics-8-F59E0B?style=for-the-badge)](#project-index)
[![Power BI](https://img.shields.io/badge/Power_BI-6-F2C811?style=for-the-badge&logo=powerbi&logoColor=111827)](#project-index)
[![Tableau](https://img.shields.io/badge/Tableau-6-E97627?style=for-the-badge&logo=tableau&logoColor=white)](#project-index)

A recruiter-friendly collection of 50 compact, reproducible analytics case studies by **Md Adib Azam**. Each project starts with a business question, identifies decision-ready KPIs, links to source data and includes a tool-specific deliverable.

## Coverage

| Track | Projects | Evidence |
|---|---:|---|
| Excel | 10 | formulas, PivotTable plan, validation and dashboard blueprints |
| SQL | 10 | executable analytical queries, CTEs and window functions |
| Python | 10 | pandas/NumPy scripts for EDA, quality, segmentation and forecasting |
| Statistics | 8 | hypothesis tests, confidence intervals, effect sizes and regression |
| Power BI | 6 | DAX measure packs and dashboard interaction blueprints |
| Tableau | 6 | calculated fields and multi-dashboard story blueprints |

## Run locally

```bash
python -m pip install -r requirements.txt
python 21-retail-eda-python/analysis.py
python verify_portfolio.py
```

The five CSV files in [`datasets/`](datasets/) are deliberately compact and auditable. They make the calculations reproducible without hiding logic inside large downloads.

## Project index

| # | Project | Tool | Business question |
|---:|---|---|---|
| 01 | [Retail Sales KPI Dashboard](01-sales-kpi-dashboard/) | Excel | Which regions and categories drive net sales? |
| 02 | [Monthly Budget Variance Tracker](02-monthly-budget-variance/) | Excel | Which channels are over budget relative to return? |
| 03 | [Inventory Reorder Analysis](03-inventory-reorder-analysis/) | Excel | Which products need priority replenishment? |
| 04 | [Customer Segmentation Pivot Report](04-customer-segmentation-pivot/) | Excel | How does spend vary by city and segment? |
| 05 | [Support SLA Scorecard](05-support-sla-scorecard/) | Excel | Where are response-time and closure bottlenecks? |
| 06 | [HR Attrition Workbook](06-hr-attrition-workbook/) | Excel | Which workforce groups have the highest attrition? |
| 07 | [Marketing Campaign ROI Model](07-campaign-roi-model/) | Excel | Which campaigns produce the strongest return? |
| 08 | [Excel Sales Forecast Sheet](08-sales-forecast-sheet/) | Excel | What is the baseline next-period sales forecast? |
| 09 | [Excel Data Cleaning Audit](09-data-cleaning-audit/) | Excel | Which records fail completeness and validity checks? |
| 10 | [Executive Performance Pack](10-executive-performance-pack/) | Excel | What are the headline commercial trends? |
| 11 | [Retail Sales Analysis with SQL](11-retail-sales-sql/) | SQL | How do revenue and order value rank across regions? |
| 12 | [Customer Lifetime Value SQL](12-customer-lifetime-value-sql/) | SQL | Which customers contribute the most sales value? |
| 13 | [Support Ticket SLA SQL](13-support-ticket-sla-sql/) | SQL | Which agents and channels miss response targets? |
| 14 | [Employee Attrition SQL](14-employee-attrition-sql/) | SQL | Which departments show elevated employee exits? |
| 15 | [Marketing Funnel SQL](15-marketing-funnel-sql/) | SQL | Where does the funnel lose efficiency? |
| 16 | [Customer Cohort SQL](16-cohort-retention-sql/) | SQL | How do signup cohorts differ in churn and spend? |
| 17 | [Product Affinity SQL](17-product-affinity-sql/) | SQL | Which category combinations are valuable? |
| 18 | [Regional Performance Ranking SQL](18-regional-ranking-sql/) | SQL | How do regions rank after discount-adjusted sales? |
| 19 | [Support Agent Workload SQL](19-agent-workload-sql/) | SQL | Is support workload distributed fairly? |
| 20 | [Salary Benchmark SQL](20-salary-benchmark-sql/) | SQL | Who falls above or below department benchmarks? |
| 21 | [Retail Exploratory Data Analysis](21-retail-eda-python/) | Python | What patterns and outliers exist in retail sales? |
| 22 | [Customer Churn Risk Analysis](22-churn-risk-python/) | Python | Which customer characteristics signal churn risk? |
| 23 | [Support Ticket Trend Analysis](23-ticket-volume-python/) | Python | How do ticket load and response vary by channel? |
| 24 | [Employee Workforce Analytics](24-employee-analytics-python/) | Python | How are performance, pay and attrition related? |
| 25 | [Campaign Performance Optimizer](25-campaign-optimizer-python/) | Python | How should budget be prioritized by campaign efficiency? |
| 26 | [Python Sales Forecast Baseline](26-sales-forecast-python/) | Python | What does a transparent trend forecast predict? |
| 27 | [Rule-Based Customer Clustering](27-customer-clustering-python/) | Python | How can customers be grouped into actionable tiers? |
| 28 | [Sales Anomaly Detection](28-anomaly-detection-python/) | Python | Which orders are unusual using robust statistics? |
| 29 | [Automated Data Quality Report](29-automated-data-quality-python/) | Python | Can quality failures be detected reproducibly? |
| 30 | [Multi-Source Business Report](30-multi-source-business-report/) | Python | Can marketing efficiency be summarized automatically? |
| 31 | [A/B Test Conversion Analysis](31-ab-test-conversion/) | Statistics | Is the conversion-rate difference statistically meaningful? |
| 32 | [Salary Confidence Interval](32-salary-confidence-interval/) | Statistics | What range likely contains the workforce mean salary? |
| 33 | [Customer Spend Correlation Study](33-spend-correlation-study/) | Statistics | How strongly are age, satisfaction and spend related? |
| 34 | [Attrition Chi-Square Test](34-attrition-chi-square/) | Statistics | Is overtime associated with attrition? |
| 35 | [Sales Distribution Analysis](35-sales-distribution-analysis/) | Statistics | How variable and skewed are order values? |
| 36 | [CSAT Hypothesis Test](36-csat-hypothesis-test/) | Statistics | Does mean CSAT meet the service target? |
| 37 | [Bootstrap ROAS Confidence Interval](37-bootstrap-roas/) | Statistics | How uncertain is the average campaign ROAS? |
| 38 | [Customer Spend Regression](38-regression-spend-model/) | Statistics | How much spend variation is explained by satisfaction? |
| 39 | [Power BI Sales Command Center](39-powerbi-sales-command-center/) | Power BI | How is net sales tracking across regions and categories? |
| 40 | [Power BI Customer Health Dashboard](40-powerbi-customer-health/) | Power BI | Where are churn and satisfaction risks concentrated? |
| 41 | [Power BI Service Operations Dashboard](41-powerbi-service-operations/) | Power BI | Which operational queues need intervention? |
| 42 | [Power BI Workforce Insights](42-powerbi-workforce-insights/) | Power BI | What factors accompany attrition and performance? |
| 43 | [Power BI Marketing ROI Dashboard](43-powerbi-marketing-roi/) | Power BI | Which channels convert spend into revenue efficiently? |
| 44 | [Power BI Executive Scorecard](44-powerbi-executive-scorecard/) | Power BI | What should leadership see in a one-page scorecard? |
| 45 | [Tableau Retail Sales Story](45-tableau-sales-story/) | Tableau | What geographic and product story explains sales? |
| 46 | [Tableau Customer Segment Explorer](46-tableau-customer-segments/) | Tableau | How do customer segments differ by value and churn? |
| 47 | [Tableau Support Operations Monitor](47-tableau-support-monitor/) | Tableau | Where do response delays affect satisfaction? |
| 48 | [Tableau HR Attrition Story](48-tableau-hr-story/) | Tableau | Which employee groups require retention action? |
| 49 | [Tableau Campaign Performance](49-tableau-campaign-analysis/) | Tableau | Which channels win on reach and return? |
| 50 | [Tableau Executive Business Overview](50-tableau-executive-overview/) | Tableau | How can leaders explore performance in three clicks? |

## Honest scope

Power BI `.pbix` files are proprietary binaries and Tableau packaged workbooks require desktop authoring. These projects provide the complete source data, DAX/calculated fields, visual layout, interactions and QA checklist needed to reproduce the dashboards in the respective desktop tools; they do not pretend a binary dashboard was generated or published when it was not.

## Author

**Md Adib Azam** — Computer Science & Technology student focused on practical data analytics and decision-ready reporting.
