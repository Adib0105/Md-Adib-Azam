# Workbook Blueprint

## Calculations

- Net Sales: `=[@units]*[@unit_price]*(1-[@discount])`
- AOV: `=SUM(NetSales)/COUNTA(UNIQUE(order_id))`
- Region selector: Data Validation + `SUMIFS`
- Build PivotTables for Region and Category; add timeline and slicers.

## Required sheets

1. `Raw_Data` — untouched CSV import
2. `Calculations` — helper columns and checks
3. `Dashboard` — KPI cards, charts, filters and a one-sentence recommendation
