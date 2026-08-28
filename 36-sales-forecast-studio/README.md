# Sales Forecast Studio

A transparent command-line forecasting baseline for monthly sales data.

## What I built

- CSV input with month and sales fields
- Three-period moving average for recent-level context
- Least-squares linear trend for future estimates
- Two-period holdout mean absolute error for a simple reality check
- Correct future month labels across year boundaries
- Structured JSON output for reporting or automation

## Current sample result

The included eight-month dataset produces:

- Three-period moving average: **161,000**
- Holdout MAE: **519.04**
- Forecasts for the next three calendar months

## Run and verify

```bash
python app.py sample_sales.csv --periods 3
python test.py
```

Tests cover the trend calculation, moving average, December-to-January rollover and a perfectly linear sample.

## Scope

This is an understandable baseline for short series. A production forecast would compare seasonality, promotions, confidence intervals and multiple validation windows.

[Back to flagship case studies](../PORTFOLIO_SHOWCASE.md)
