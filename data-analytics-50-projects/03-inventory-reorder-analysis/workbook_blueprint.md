# Workbook Blueprint

## Calculations

- Sales Velocity: `=SUMIFS(units,product,[@product])`
- Reorder Flag: `=IF([@SalesVelocity]>=4,"REORDER","OK")`
- Rank products by velocity with `RANK.EQ`.

## Required sheets

1. `Raw_Data` — untouched CSV import
2. `Calculations` — helper columns and checks
3. `Dashboard` — KPI cards, charts, filters and a one-sentence recommendation
