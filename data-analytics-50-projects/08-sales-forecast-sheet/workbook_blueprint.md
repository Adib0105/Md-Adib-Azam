# Workbook Blueprint

## Calculations

- Monthly Revenue: group Date by Month in a PivotTable.
- 3-period MA: `=AVERAGE(B2:B4)`
- Growth: `=IFERROR(B4/B3-1,0)`
- Use `FORECAST.LINEAR` for a transparent baseline.

## Required sheets

1. `Raw_Data` — untouched CSV import
2. `Calculations` — helper columns and checks
3. `Dashboard` — KPI cards, charts, filters and a one-sentence recommendation
