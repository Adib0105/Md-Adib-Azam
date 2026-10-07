# JobMatch upgrade report — A–P

Repository: `Adib0105/Md-Adib-Azam` · Application: `job-recommendation-system/` · Baseline: `926f82c2f7235af2e2a150bbd053a87a54d04bfd` · Date: 7 October 2026.

## A. What already existed

Flask/SQLAlchemy/SQLite application, reviewed PDF/DOCX extraction, candidate profiles, seven-factor TF-IDF ranking, skill analysis, career simulator, saved jobs, application statuses, immutable recommendation history, eight dataset charts, basic admin CRUD, 640 synthetic jobs, local fonts/assets, 60 backend tests and a browser workflow. See [the audit](UPGRADE_AUDIT.md).

## B. What changed

Signed-cookie-only authentication became revocable, token-hashed server sessions. Fixed administrator seeding was removed; legacy public demo admin is disabled on upgrade. Demo candidate creation now uses a generated password. SQL filters bound catalog ranking, salary comparisons respect currency/pay period, external unknown fields stay neutral, equal scores use explicit context tie-breakers, and model cache writes use unique temporary files. Existing record relationships, original scoring components and offline functionality remain.

## C. What was added

Official Adzuna and optional USAJOBS adapters; safe normalized external jobs; canonical/source-identity deduplication; TTL caches, leases, budgets and fallback; freshness and source UI; Google outbound search; remembered sessions, password recovery/change, email verification and session management; notification center, daily/weekly alert worker, tracker details and resume-job comparison; admin providers, lifecycle/bulk CSV, account suspension, analytics, CMS, validated settings, email/health, security/audit and private backups. Added global discovery/search, accessible marquee, About/developer card and college credits using bundled typography.

## D. Files created

- [`docs/UPGRADE_AUDIT.md`](../docs/UPGRADE_AUDIT.md)
- [`docs/UPGRADE_REPORT.md`](../docs/UPGRADE_REPORT.md)
- [`docs/screenshots/about-desktop.png`](../docs/screenshots/about-desktop.png)
- [`docs/screenshots/discovery-desktop.png`](../docs/screenshots/discovery-desktop.png)
- [`docs/screenshots/providers-desktop.png`](../docs/screenshots/providers-desktop.png)
- [`routes/control.py`](../routes/control.py)
- [`routes/public.py`](../routes/public.py)
- [`routes/workspace.py`](../routes/workspace.py)
- [`scripts/process_alerts.py`](../scripts/process_alerts.py)
- [`scripts/sync_jobs.py`](../scripts/sync_jobs.py)
- [`scripts/upgrade_database.py`](../scripts/upgrade_database.py)
- [`services/account_service.py`](../services/account_service.py)
- [`services/alert_service.py`](../services/alert_service.py)
- [`services/external_jobs_service.py`](../services/external_jobs_service.py)
- [`services/job_catalog.py`](../services/job_catalog.py)
- [`services/job_providers/__init__.py`](../services/job_providers/__init__.py)
- [`services/job_providers/adzuna_provider.py`](../services/job_providers/adzuna_provider.py)
- [`services/job_providers/base.py`](../services/job_providers/base.py)
- [`services/job_providers/provider_registry.py`](../services/job_providers/provider_registry.py)
- [`services/job_providers/usajobs_provider.py`](../services/job_providers/usajobs_provider.py)
- [`services/logging_service.py`](../services/logging_service.py)
- [`services/mail_service.py`](../services/mail_service.py)
- [`services/notification_service.py`](../services/notification_service.py)
- [`services/schema_service.py`](../services/schema_service.py)
- [`services/security_service.py`](../services/security_service.py)
- [`services/settings_service.py`](../services/settings_service.py)
- [`static/css/discovery.css`](../static/css/discovery.css)
- [`static/js/discovery.js`](../static/js/discovery.js)
- [`templates/about.html`](../templates/about.html)
- [`templates/account/recovery.html`](../templates/account/recovery.html)
- [`templates/account/settings.html`](../templates/account/settings.html)
- [`templates/admin/analytics.html`](../templates/admin/analytics.html)
- [`templates/admin/backups.html`](../templates/admin/backups.html)
- [`templates/admin/content.html`](../templates/admin/content.html)
- [`templates/admin/health.html`](../templates/admin/health.html)
- [`templates/admin/providers.html`](../templates/admin/providers.html)
- [`templates/admin/records.html`](../templates/admin/records.html)
- [`templates/admin/settings.html`](../templates/admin/settings.html)
- [`templates/alerts.html`](../templates/alerts.html)
- [`templates/info.html`](../templates/info.html)
- [`templates/notifications.html`](../templates/notifications.html)
- [`templates/resume_compare.html`](../templates/resume_compare.html)
- [`tests/fixtures/v1_schema.sql`](../tests/fixtures/v1_schema.sql)
- [`tests/test_control_workspace.py`](../tests/test_control_workspace.py)
- [`tests/test_migration.py`](../tests/test_migration.py)
- [`tests/test_providers.py`](../tests/test_providers.py)
- [`tests/test_security_upgrade.py`](../tests/test_security_upgrade.py)
- [`tests/test_setup_commands.py`](../tests/test_setup_commands.py)

## E. Files modified

- [`.env.example`](../.env.example)
- [`.github/workflows/tests.yml`](../.github/workflows/tests.yml)
- [`README.md`](../README.md)
- [`START_HERE_HINGLISH.md`](../START_HERE_HINGLISH.md)
- [`app.py`](../app.py)
- [`config.py`](../config.py)
- [`data/processed_jobs.csv`](../data/processed_jobs.csv)
- [`docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md)
- [`docs/VALIDATION.md`](../docs/VALIDATION.md)
- [`docs/screenshots/browser-results.json`](../docs/screenshots/browser-results.json)
- [`docs/screenshots/dashboard-desktop.png`](../docs/screenshots/dashboard-desktop.png)
- [`docs/screenshots/dashboard-mobile.png`](../docs/screenshots/dashboard-mobile.png)
- [`docs/screenshots/insights-desktop.png`](../docs/screenshots/insights-desktop.png)
- [`docs/screenshots/job-match-desktop.png`](../docs/screenshots/job-match-desktop.png)
- [`docs/screenshots/landing-desktop.png`](../docs/screenshots/landing-desktop.png)
- [`docs/screenshots/simulator-desktop.png`](../docs/screenshots/simulator-desktop.png)
- [`models/database.py`](../models/database.py)
- [`models/recommendation_model.py`](../models/recommendation_model.py)
- [`routes/admin.py`](../routes/admin.py)
- [`routes/auth.py`](../routes/auth.py)
- [`routes/candidate.py`](../routes/candidate.py)
- [`routes/jobs.py`](../routes/jobs.py)
- [`routes/recommendations.py`](../routes/recommendations.py)
- [`scripts/create_admin.py`](../scripts/create_admin.py)
- [`scripts/seed_database.py`](../scripts/seed_database.py)
- [`scripts/train_model.py`](../scripts/train_model.py)
- [`services/analytics_service.py`](../services/analytics_service.py)
- [`services/data_service.py`](../services/data_service.py)
- [`services/recommendation_service.py`](../services/recommendation_service.py)
- [`templates/admin/dashboard.html`](../templates/admin/dashboard.html)
- [`templates/admin/job_form.html`](../templates/admin/job_form.html)
- [`templates/admin/jobs.html`](../templates/admin/jobs.html)
- [`templates/admin/users.html`](../templates/admin/users.html)
- [`templates/applications.html`](../templates/applications.html)
- [`templates/auth.html`](../templates/auth.html)
- [`templates/base.html`](../templates/base.html)
- [`templates/career_insights.html`](../templates/career_insights.html)
- [`templates/dashboard.html`](../templates/dashboard.html)
- [`templates/index.html`](../templates/index.html)
- [`templates/job_details.html`](../templates/job_details.html)
- [`templates/jobs.html`](../templates/jobs.html)
- [`templates/macros.html`](../templates/macros.html)
- [`templates/methodology.html`](../templates/methodology.html)
- [`templates/profile.html`](../templates/profile.html)
- [`tests/browser_smoke.cjs`](../tests/browser_smoke.cjs)
- [`tests/conftest.py`](../tests/conftest.py)
- [`tests/test_auth.py`](../tests/test_auth.py)
- [`tests/test_recommendation.py`](../tests/test_recommendation.py)
- [`utils/constants.py`](../utils/constants.py)
- [`utils/validators.py`](../utils/validators.py)

Root `README.md` updates only the existing JobMatch feature. Root `.github/workflows/jobmatch.yml` adds diagnostic timeouts/thread limits. Other portfolio projects are untouched.

## F. Database changes

Schema v2 adds 14 tables: schema revisions, password-reset tokens, email-verification tokens, user sessions, rate-limit buckets, external identities, external cache, providers, notifications, alerts, alert deliveries, audit logs, site settings and recent job views. Existing User, Job, Application and SearchEvent receive additive fields and indexes. SQLite upgrades create an integrity-checked pre-upgrade backup and preserve records. Migration is idempotent; production requires a stopped-app maintenance command. No destructive downgrade is supplied.

## G. API integrations

Adzuna official country-based search and USAJOBS official search are implemented behind one provider interface and fixture-tested. `get_job` uses stored provider identities rather than fabricated detail endpoints. Live network calls need your valid credentials and provider terms/quota. Browser assets remain offline. Google is an outbound search link only. Provider responses and admin/public JSON APIs exclude credentials and raw private payloads.

New/read-compatible endpoints: `/api/jobs`, `/api/jobs/search`, `/api/jobs/live`, `/api/jobs/<id>`, `/api/providers`, `/api/skills`, `/api/profile`, `/api/recommendations`, `/api/notifications`, `/api/csrf`, `/api/admin/analytics`, `/api/admin/providers/health`. Password recovery uses CSRF-protected POST `/api/password/forgot` and `/api/password/reset`; existing POST `/api/recommend` remains.

## H. Environment variables

See [`.env.example`](../.env.example), which is reference-only and not auto-loaded. Main settings: `APP_ENV`, `APP_BASE_URL`, `SECRET_KEY`, `DATABASE_URL`, `JOBMATCH_INSTANCE`, `PORT`, `AUTO_UPGRADE_SCHEMA`, `SESSION_IDLE_MINUTES`, `REMEMBER_DAYS`, `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`, `USAJOBS_API_KEY`, `USAJOBS_USER_AGENT`, `ENABLE_ADZUNA`, `ENABLE_USAJOBS`, `REAL_JOB_CACHE_TTL_MINUTES`, `EXTERNAL_JOB_STALE_DAYS`, `EXTERNAL_JOB_MAX_AGE_DAYS`, `PROVIDER_REQUESTS_PER_HOUR`, `MAX_RANKING_JOBS`, `MAIL_BACKEND`, `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER`, `MAIL_USE_TLS`, `LOG_LEVEL`. No real keys or passwords are included.

## I. Security improvements

Scrypt passwords; hash-only expiring recovery/verification tokens with conditional single-use updates; revocation on security changes and suspension; idle/absolute session limits; current-password checks for password/email changes and backup downloads; database-shared rate limiting; admin and owner authorization; CSRF; escaped CMS/provider text; safe apply URLs; export formula escaping; fixed provider hosts, redirect refusal, time/size caps; private backup/dev-mail files; metadata-only JSON logs; production HTTPS, trusted Host, strong secret and secure cookie enforcement. Existing validated resume upload constraints remain. This is not a penetration-test certification.

## J. Tests added

Added suites for recovery/session security, provider transport/normalization/cache/failure/deduplication, concurrent request coalescing, v1 migration/backup integrity, control-center authorization/validation, CSRF across new writes, alert new-only/deduplicated delivery and retry, private tracker/notification ownership, verified-email rules, resume comparison, SMTP TLS ordering, admin bootstrap and backup download. Extended the original recommender tests to preserve transient-object evaluation defaults. Expanded Chromium workflow to new account/discovery/alerts/admin/mobile pages.

## K. Tests passed

**167 backend tests passed** on Linux/Python 3.12 (60 original + 107 new cases), with no warnings. Ruff lint and formatting passed; four JavaScript files passed Node syntax checks. Fresh setup seeded 640 jobs without invalid rows; model training indexed 2,287 TF-IDF features. Chromium 134 passed the expanded workflow and 28 viewport checks with zero JavaScript errors, failed resources or external browser requests. The local browser used generated test credentials and active CSRF. Evidence and reproduction steps are in [VALIDATION.md](VALIDATION.md).

Synthetic evaluation over 640 generated jobs: Precision@10 **1.0000**, Recall@10 **0.1175**, NDCG@10 **0.9804**. These authored role-family proxies reproduce the original smoke result and are not real hiring validation. Actual results are in [evaluation.json](evaluation.json).

## L. Known limitations

No real API credentials or SMTP account were supplied, so adapters/mail were verified with fixtures and a mocked TLS SMTP server, not live account delivery. No public deployment was requested or performed. SQLite is the tested database. Adzuna snippets and dictionary extraction can miss requirements; fingerprints can merge similar openings; unsupported provider filters narrow only the current page. Catalog ranking is bounded to 2,000 filtered jobs by default. Scores are lexical/rule-based estimates; context affects equal-score ties only. No deep-learning or ATS guarantee.

Alerts need an external scheduler and refreshed catalog; the CLI does not install a background service. Recovery mail uses in-process threads, and SMTP alert delivery can duplicate after a crash between acceptance and DB commit. A durable queue, stronger document-process isolation, retention jobs and deployment-specific privacy policy are future operational work. A physical Windows computer was not tested; hosted CI results are separate. The repository's unrelated portfolio gate has a pre-existing Canva folder-layout issue; it was not altered.

## M. Run locally

From `job-recommendation-system/`, create a Python 3.11/3.12 virtual environment, install `requirements.txt`, run `scripts/seed_database.py`, then `app.py`. Visit **http://127.0.0.1:5000**. Register your own candidate. Optional `--demo` creates a candidate with a generated password shown only during setup. Full Windows/Linux commands are in [README](../README.md) and [the Hinglish guide](../START_HERE_HINGLISH.md).

For an existing database, stop processes, independently back up the private instance directory, update dependencies and run `python scripts/upgrade_database.py` using the same database/instance configuration before restarting.

## N. Configure real jobs

Obtain official Adzuna credentials, set both backend environment variables, restart and test under Admin → Providers. For USAJOBS, supply its key and registered user-agent email and enable the provider. Choose country/query in Real Jobs. Missing configuration remains an honest demo fallback. Configure scheduled `scripts/sync_jobs.py` queries within provider limits if using alerts. Never put keys in GitHub or client-side code.

## O. Create the admin

Run `python scripts/create_admin.py`; supply name/email and a privately entered password. Login at `/admin/login`. To reset/reactivate an existing administrator, use `--reset-existing`; the command will not promote a candidate. It revokes prior sessions and outstanding security tokens. There is no public administrator registration or fixed administrator credential.

## P. Forgot password

Submit email at `/forgot-password`; responses stay generic. The app creates a random token, stores only its SHA-256 hash and expiry, and emails a trusted-base URL. Development mail is a private `.eml` under `instance/mail`; production requires encrypted SMTP. The form requires CSRF, a valid unexpired single-use token and a valid confirmed password. Success changes the password, invalidates old sessions and pending tokens, then requires a new login. Link fetching alone does not consume a token. Both account roles use this secure flow.
