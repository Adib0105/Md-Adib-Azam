# 25 — Website Availability Monitor

Checks a URL with Python's standard library, records status and response time, and returns a non-zero exit code when the site is unavailable. Tests use a fake opener, so they never depend on live internet.

```bash
python main.py https://example.com --timeout 5
python test_main.py
```

**Skills:** HTTP requests, timeouts, error handling, dependency injection, monitoring, standard library.
