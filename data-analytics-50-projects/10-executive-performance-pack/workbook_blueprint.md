# Workbook Blueprint

## Calculations

- Revenue: `=SUM(NetSales)`
- Orders: `=COUNTA(UNIQUE(order_id))`
- Top Region: `=INDEX(region,MATCH(MAX(region_sales),region_sales,0))`
- Arrange four KPI cards and two decision charts.

## Required sheets

1. `Raw_Data` — untouched CSV import
2. `Calculations` — helper columns and checks
3. `Dashboard` — KPI cards, charts, filters and a one-sentence recommendation
