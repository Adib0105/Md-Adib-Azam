# 41. Power BI Service Operations Dashboard

**Tool:** Power BI  
**Dataset:** [`../../datasets/support_tickets.csv`](../../datasets/support_tickets.csv)

## Business question

Which operational queues need intervention?

## KPIs

- Open Backlog
- SLA Breach
- CSAT
- Response Time

## Workflow

1. Import the linked CSV and confirm data types.
2. Check missing values, duplicate keys and invalid ranges.
3. Create the calculations in `measures.dax`.
4. Validate totals against a simple grouped summary.
5. Present one decision, supported by the KPI output.

## Deliverable

Open [`measures.dax`](measures.dax) for the reproducible analysis. The source data is intentionally small so every result can be checked manually before scaling to a larger dataset.

## Portfolio talking point

This project demonstrates how I translate a business question into clean metrics, a repeatable analysis and a decision-ready output using Power BI.
