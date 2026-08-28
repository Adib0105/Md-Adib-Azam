# Md Adib Azam — Flagship Project Showcase

This is the short, evidence-first route through my portfolio. It highlights the projects that best demonstrate how I approach a problem, implement the solution and verify the result.

> All datasets and example records in these projects are synthetic. Metrics are reproducible demonstrations, not claims about a real employer or client system.

## Five-minute review path

1. Open [JARVIS AI OMEGA V7.5](#featured-build--jarvis-ai-omega-v75) for the largest standalone agent project.
2. Continue with the [Advanced Data Analytics collection](#1-advanced-data-analytics-portfolio) for end-to-end analytical depth.
3. Review the [Customer Support SLA Dashboard](#2-customer-support-sla-dashboard) and [Digital Seva Workflow](#3-digital-seva-request-workflow) for practical operations work.
4. Open the [MySQL Helpdesk Database](#4-mysql-helpdesk-database) for relational design.
5. Finish with the [Security Header Auditor](#6-defensive-security-header-auditor) and [Excel Dashboard](#8-excel-sales-dashboard-workbook) for breadth.

## Evidence summary

| Quality gate | Result | Reproduce |
|---|---:|---|
| Resume-aligned technical collection | 275 working projects | `python resume-projects-400/verify_portfolio.py` |
| CV-aligned multi-file applications | 20/20 passed | `python run_cv_project_tests.py` |
| Advanced analytics pipelines | 20/20 completed | `python advanced-data-analytics/run_all.py` |
| Creative/media spaces | 125 clean folders | Preserved for Md Adib Azam's finished files |

## Featured build — JARVIS AI OMEGA V7.5

**JARVIS AI OMEGA** is a separate Windows-first multimodal desktop-agent project organized around a strict runtime loop:

```text
UNDERSTAND → PLAN → PERMISSION → EXECUTE → VERIFY → RECOVER / REPLAN
```

Its documented scope includes Hindi/Hinglish/English voice interaction, screen and image vision, layered memory and RAG, capability-aware computer use, browser research, coding tools, observability, security gates and controlled self-development workflows.

The repository also documents capability status, testing across multiple Python versions, Windows packaging, audit boundaries and features that still require real-workstation validation.

**Review the complete standalone project:** [Adib0105/JARVIS-AI-OMEGA](https://github.com/Adib0105/JARVIS-AI-OMEGA)

## 1. Advanced Data Analytics Portfolio

**Problem.** A portfolio can list algorithms without showing whether they answer a useful business question. This collection connects each method to a decision, a measurable result and a reproducible output.

**Implementation.** Twenty independent Python pipelines generate deterministic synthetic data, train or calculate the relevant model, evaluate it with business-aware metrics and write a machine-readable metrics file plus a decision brief.

**Selected evidence from a complete run:**

- Inventory optimization raised simulated service level from **49.93% to 94.94%**.
- CUPED reduced experiment variance by **66.12%** with a measured **3.53% uplift**.
- Energy forecasting achieved **3.99% MAPE** on the generated evaluation set.
- Predictive-maintenance prioritization estimated **₹1,845,200** in net savings under the stated simulation assumptions.

**Review:** [Collection overview](advanced-data-analytics/) · [Project source](advanced-data-analytics/projects/) · [Generated artifacts](advanced-data-analytics/artifacts/)

```bash
python advanced-data-analytics/run_all.py
```

## 2. Customer Support SLA Dashboard

**Problem.** Support teams need an immediate view of open tickets, SLA breaches, first-response time and agent workload.

**Implementation.** The responsive interface keeps presentation separate from reusable JavaScript business logic. The logic calculates unresolved workload, detects tickets older than their SLA allowance and aggregates agent assignments.

**Verification.** The Node test exercises KPI and workload calculations and currently reports `SLA dashboard tests passed`.

**Review:** [Project folder](28-customer-support-sla-dashboard/) · [Business logic](28-customer-support-sla-dashboard/logic.js) · [Automated test](28-customer-support-sla-dashboard/test.js)

```bash
cd 28-customer-support-sla-dashboard
node test.js
```

## 3. Digital Seva Request Workflow

**Problem.** A digital service centre needs a simple way to record customer requests and move each one through a controlled delivery process.

**Implementation.** The browser application validates customer and service fields, persists records locally, supports search and restricts progress to four ordered states: Received, In progress, Ready and Delivered.

**Verification.** Tests cover input validation, valid status progression and operational summary counts.

**Review:** [Project folder](30-digital-seva-workflow/) · [Workflow rules](30-digital-seva-workflow/logic.js) · [Automated test](30-digital-seva-workflow/test.js)

```bash
cd 30-digital-seva-workflow
node test.js
```

## 4. MySQL Helpdesk Database

**Problem.** Customer support data needs consistent relationships, fast queue queries and reusable SLA reporting.

**Implementation.** The MySQL 8 design models customers, agents, tickets, messages and tags. It includes foreign keys, uniqueness constraints, resolution-order validation, cascading message/tag cleanup, queue indexes and two reporting views.

**Verification.** The validator checks the required schema objects and currently reports `MySQL helpdesk schema validation passed`.

**Review:** [Project folder](37-mysql-helpdesk-schema/) · [Schema](37-mysql-helpdesk-schema/schema.sql) · [Analytical queries](37-mysql-helpdesk-schema/queries.sql)

```bash
cd 37-mysql-helpdesk-schema
python validate_schema.py
```

## 5. Sales Forecast Studio

**Problem.** A small business needs a transparent baseline forecast that can be understood without a black-box platform.

**Implementation.** The command-line tool reads monthly sales from CSV, calculates a three-period moving average, fits a least-squares linear trend and evaluates the trend on a two-period holdout.

**Current sample result.** Eight observations produce a holdout MAE of **519.04** and three dated future estimates in JSON.

**Review:** [Project folder](36-sales-forecast-studio/) · [Forecast implementation](36-sales-forecast-studio/app.py) · [Sample data](36-sales-forecast-studio/sample_sales.csv)

```bash
cd 36-sales-forecast-studio
python app.py sample_sales.csv --periods 3
python test.py
```

## 6. Defensive Security Header Auditor

**Problem.** Web projects need a safe way to review saved response-header configuration without scanning a live target.

**Implementation.** The offline Python checker normalizes header names, evaluates five browser-security controls, validates HSTS duration and returns clear remediation guidance in JSON.

**Current sample result.** The included secure example passes **5/5 checks** for a score of **100**. The tool explicitly limits its scope to offline configuration review.

**Review:** [Project folder](38-security-header-auditor/) · [Audit logic](38-security-header-auditor/app.py) · [Automated test](38-security-header-auditor/test.py)

```bash
cd 38-security-header-auditor
python app.py sample_headers.json
python test.py
```

## 7. Explainable Resume–Job Matcher

**Problem.** Keyword-match tools often return a number without explaining what produced it.

**Implementation.** This local Python project tokenizes resume and job text, weights repeated job terms, reports matched and missing keywords and recommends adding only skills supported by real evidence. It needs no API key.

**Current sample result.** The included resume and role produce a **42.9%** match with separate matched and missing lists, making the recommendation auditable.

**Review:** [Project folder](26-ai-resume-job-matcher/) · [Matching logic](26-ai-resume-job-matcher/app.py) · [Automated test](26-ai-resume-job-matcher/test.py)

```bash
cd 26-ai-resume-job-matcher
python app.py sample_resume.txt sample_job.txt
python test.py
```

## 8. Excel Sales Dashboard Workbook

**Problem.** Operational users often need a familiar workbook instead of a code-only report.

**Implementation.** The Excel file contains structured data, formulas, KPI output and a native chart. It is one of 25 real XLSX workbooks in the collection.

**Verification.** This workbook contains **45 formulas**, two worksheets, a native chart and a rendered preview. Across the Excel track there are at least **900 formulas and 25 charts**.

**Review:** [Project folder](resume-projects-400/10-excel-ms-office/01-sales-dashboard-workbook/) · [Workbook preview](resume-projects-400/10-excel-ms-office/01-sales-dashboard-workbook/preview.png)

## More projects worth reviewing

- [Responsive Developer Portfolio](40-responsive-portfolio-site/)
- [Support Ticket Intelligence](27-support-ticket-intelligence/)
- [Student Records with SQLite](29-student-records-sqlite/)
- [Mini CRM Lead Manager](31-mini-crm-lead-manager/)
- [Access Log Threat Monitor](39-access-log-threat-monitor/)
- [Automation Report Generator](45-automation-report-generator/)

---

[Back to the main portfolio](README.md) · [Browse all 400 items](resume-projects-400/PROJECT_INDEX.md) · [Read the quality report](resume-projects-400/QUALITY_REPORT.md)
