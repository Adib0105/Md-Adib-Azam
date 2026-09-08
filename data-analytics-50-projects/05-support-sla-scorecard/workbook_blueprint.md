# Workbook Blueprint

## Calculations

- SLA Flag: `=IF([@first_response_min]>30,"BREACH","MET")`
- Open Flag: `=--([@status]="Open")`
- Summarize by agent and channel using PivotTables.

## Required sheets

1. `Raw_Data` — untouched CSV import
2. `Calculations` — helper columns and checks
3. `Dashboard` — KPI cards, charts, filters and a one-sentence recommendation
