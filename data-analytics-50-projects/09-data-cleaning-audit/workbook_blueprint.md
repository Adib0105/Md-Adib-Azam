# Workbook Blueprint

## Calculations

- Missing Check: `=COUNTBLANK(A2:H11)`
- Duplicate ID: `=COUNTIF(customer_id,[@customer_id])>1`
- Valid Age: `=AND([@age]>=18,[@age]<=100)`.

## Required sheets

1. `Raw_Data` — untouched CSV import
2. `Calculations` — helper columns and checks
3. `Dashboard` — KPI cards, charts, filters and a one-sentence recommendation
