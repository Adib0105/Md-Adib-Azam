# Digital Seva Request Workflow

A browser-based request tracker for documentation, application and customer follow-up work at a digital service centre.

## What I built

- Request creation with customer and service validation
- A controlled four-step lifecycle: `Received → In progress → Ready → Delivered`
- Search and status summaries for day-to-day queue review
- Local browser persistence so requests survive a page refresh
- Separate workflow rules that can be tested without the interface

The state function never advances a delivered request and never invents a status outside the defined sequence.

## Run and verify

```bash
node test.js
```

Then open `index.html` in a browser. Tests cover state progression, final-state protection, validation and summary counts.

## Files

- `index.html` — form and request list
- `style.css` — responsive layout
- `logic.js` — validation, state and summary rules
- `app.js` — storage and UI behaviour
- `test.js` — Node assertions

## Scope

This version is designed for a single browser profile. A production multi-user system would add authentication, a server-side database and audit history.

[Back to flagship case studies](../PORTFOLIO_SHOWCASE.md)
