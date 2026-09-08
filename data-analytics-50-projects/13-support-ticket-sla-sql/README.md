# 13. Support Ticket SLA SQL

**Tool:** SQL  
**Dataset:** [`../../datasets/support_tickets.csv`](../../datasets/support_tickets.csv)

## Business question

Which agents and channels miss response targets?

## KPIs

- Tickets
- Avg Response
- Breach Rate
- CSAT

## Workflow

1. Import the linked CSV and confirm data types.
2. Check missing values, duplicate keys and invalid ranges.
3. Create the calculations in `analysis.sql`.
4. Validate totals against a simple grouped summary.
5. Present one decision, supported by the KPI output.

## Deliverable

Open [`analysis.sql`](analysis.sql) for the reproducible analysis. The source data is intentionally small so every result can be checked manually before scaling to a larger dataset.

## Portfolio talking point

This project demonstrates how I translate a business question into clean metrics, a repeatable analysis and a decision-ready output using SQL.
