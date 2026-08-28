# Customer Support SLA Dashboard

A responsive operations dashboard for reviewing ticket volume, SLA risk, first-response time and agent workload.

## What I built

- KPI cards for total tickets, unresolved work, SLA breaches and average first response
- Status filtering for fast queue review
- Agent-level unresolved workload summary
- Reusable business logic separated from DOM rendering
- Responsive layout for desktop and mobile widths

## Metric rules

- A ticket is **open** when its status is not `Resolved`.
- An open ticket is **breached** when `ageHours > slaHours`.
- Average first response is calculated across every supplied ticket and rounded to minutes.
- Workload counts only unresolved tickets assigned to each agent.

## Run and verify

```bash
node test.js
```

Then open `index.html` in a browser. The automated test covers open-ticket count, breach detection, response average and agent workload; the current result is `SLA dashboard tests passed`.

## Files

- `index.html` — semantic dashboard structure
- `style.css` — responsive visual system
- `logic.js` — testable KPI calculations
- `app.js` — sample data, filters and rendering
- `test.js` — Node assertions

All ticket records are synthetic.

[Back to flagship case studies](../PORTFOLIO_SHOWCASE.md)
