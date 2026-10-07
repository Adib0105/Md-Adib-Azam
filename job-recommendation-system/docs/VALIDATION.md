# Validation record — 7 October 2026

Environment: Linux, Python 3.12, exact pinned dependencies in an isolated virtual environment, Playwright 1.51.1 and headless Chromium **134.0.6998.35**. No real provider credentials or SMTP account were supplied.

## Automated checks

**167 automated tests passed**. The completed upgrade test result and file inventory are recorded in [UPGRADE_REPORT.md](UPGRADE_REPORT.md). The suite includes all 60 original tests and new security, provider, migration, admin, alert and account checks. Ruff formatting/lint and Node syntax checks are included in the final verification.

Coverage includes generic recovery responses, hash-only tokens, expiry, single use, old-session revocation, admin reset, trusted-origin links, current-password checks, verified email changes, security-token invalidation, remember/idle limits, persistent rate limits, public/admin separation, CSRF on new writes, safe URLs, CSV injection prevention and private backups.

Provider tests use deterministic fixtures from the documented response shapes: normalization, parameters, currency/pay-period honesty, unknown fields, malformed rows, safe transport failures, response size cap, redirect refusal, TTL hit/expiry, shared leases, simultaneous duplicate searches, hourly budget, source/fingerprint deduplication, cached failure fallback, missing credentials and stale exclusion. They **do not establish that a real API account is connected**.

A v1-schema fixture upgrades while preserving profile/resume text, password hashes, jobs and application status; verifies the pre-upgrade SQLite backup and integrity; verifies idempotence and the explicit production-style migration gate. No live user database was used for these tests.

## Browser evidence

`docs/screenshots/browser-results.json` records the actual browser version, checked widths and workflow. Generated candidate/admin test passwords are supplied through the test process environment; there are no default admin credentials in the test script.

Passed with real form submissions and active CSRF:

- Landing, locally bundled fonts, normal animation, live reduced-motion cancellation and JavaScript-disabled landing.
- Candidate login, dashboard, detailed matching explanation and all eight charts.
- Fresh registration, profile save with skill tags, DOCX upload, extraction review and confirmation.
- Recommendations, saved job, local tracker, Interview status, notes and follow-up date.
- Resume-versus-job comparison, alert creation and account session page.
- Simulator, match history and logout.
- Separate admin login, job create/edit/soft-delete and control-center pages.
- Real discovery without credentials shows the explicit connection/fallback message and demo labels.
- About/developer/college credits and source-aware UI.

**28 viewport checks passed**, including 390 px candidate pages and administrator controls, with no document-level horizontal overflow. The run recorded **zero JavaScript errors, zero failed HTTP resources and zero external browser requests**. Local UI assets work without a CDN; outbound apply/Google links are not followed by the test. Backend provider fixtures verify their destination safety.

Screenshots of landing, dashboard/mobile, job explanation, discovery, providers, About, charts and simulator were captured. Landing, About and mobile dashboard were visually inspected for layout.

Reproduce the optional browser test against a disposable local instance:

```bash
npm install --no-save playwright@1.51.1
npx playwright install chromium --only-shell
# Set TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD and TEST_DEMO_PASSWORD to
# accounts you created only for this test. Set RESUME_FIXTURE to a test DOCX.
node tests/browser_smoke.cjs
```

The script assumes a candidate `demo@jobmatch.com` and the supplied test admin. It creates extra candidates/jobs. Do not use an important personal instance for destructive QA. `TEST_BASE_URL` defaults to loopback and `SCREENSHOT_DIR` controls evidence output.

## Limits of this evidence

No physical Windows computer, production HTTPS host, real Adzuna/USAJOBS account or real SMTP delivery was exercised. GitHub Actions has a Linux/Windows × Python 3.11/3.12 matrix; linked runs are the authority for hosted-runner status. Each job now has a 15-minute limit and pytest faulthandler output to diagnose stalls. A separate repository portfolio gate is outside this app's scope.

This is not an independent penetration test, accessibility certification, load test, real hiring-outcome study or exactly-once SMTP guarantee. The original synthetic evaluation remains a model sanity check; its authored role-family labels do not establish fairness or generalization. No unsupported claims about hiring accuracy or live provider availability are made.
