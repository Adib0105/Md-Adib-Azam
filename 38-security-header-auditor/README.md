# Defensive Security Header Auditor

A safe offline checker for reviewing a saved set of HTTP response headers.

## What I built

The tool normalizes header names and evaluates five browser-security controls:

1. Content Security Policy
2. HTTP Strict Transport Security
3. X-Content-Type-Options
4. Referrer Policy
5. Permissions Policy

HSTS passes only when it contains a numeric `max-age` of at least 31,536,000 seconds, and X-Content-Type-Options passes only with `nosniff`. Missing or weak values receive a specific remediation message.

## Run and verify

```bash
python app.py sample_headers.json
python test.py
```

The included secure example scores **100/100 (5/5 checks)**. Tests also verify that weak HSTS and an incorrect content-type option fail.

## Safety boundary

This project reads a local JSON file only. It performs no live scanning, exploitation, credential collection or unauthorized network activity.

[Back to flagship case studies](../PORTFOLIO_SHOWCASE.md)
