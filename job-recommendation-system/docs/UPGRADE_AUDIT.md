# Upgrade audit — 7 October 2026

Baseline: repository commit `926f82c2f7235af2e2a150bbd053a87a54d04bfd`.
Scope: the existing JobMatch subfolder, its workflow, and its portfolio entry. No repository AGENTS.md was present. The separate 400-item portfolio gate has an existing Canva folder-layout mismatch; those projects are outside this upgrade.

## Existing implementation

- Flask application factory; loopback Waitress startup; CSRF, escaping, safe redirect targets and security headers.
- Separate candidate/admin login; scrypt password hashes; in-process throttling; signed cookie sessions.
- Tables: users, candidate_skills, jobs, saved_jobs, applications, recommendation_runs, recommendations, resume_drafts, search_events.
- Candidate profile, reviewed PDF/DOCX extraction, skills, saved jobs, local tracker, career charts, simulator, immutable match snapshots.
- Seven weighted components: skills, TF-IDF text similarity, experience, education, location, salary and preferred role. Job-feature caches and deterministic explanations already exist.
- Administrator job CRUD and candidate overview. Soft removal preserves tracker/history references.
- Bundled Bootstrap, Font Awesome, Chart.js, Manrope and Fraunces; reusable cards/forms; responsive layouts and reduced motion.
- 640 explicitly synthetic jobs, 60 backend tests and a Chromium workflow. Linux CI passed. The old Windows jobs were still running at audit time; their completion cannot be claimed.

## Audit findings and implementation checklist

| Area | Gap / risk | Upgrade direction |
| --- | --- | --- |
| Schema | `create_all` does not upgrade existing columns | Versioned additive migration, SQLite backup, legacy-data regression test |
| Authentication | No reset/change password, session revocation or account suspension | Hashed single-use reset tokens, trusted-base URLs, server-side sessions and activity |
| Administrator setup | Opt-in seed and documentation expose a fixed demo administrator | Remove fixed admin bootstrap; disable the legacy demo administrator during migration; interactive reset/create command |
| Rate limiting | Process-local attempt dictionary does not span workers | Atomic database-backed hashed rate-limit buckets |
| External jobs | No providers, attribution, cache or lifecycle metadata | Official Adzuna/USAJOBS adapters, normalized records, TTL cache and request leases |
| Deduplication | Dataset-only duplicate cleaning | Unique provider IDs plus canonical fingerprints and source aliases |
| Scoring | INR-only salary assumptions; no freshness/remote context | Preserve seven scores; neutral unknown/mismatched currency; explain preference/freshness ranking context |
| Queries | Several pages load all records before pagination | SQL filters, bounded recommendation pool, database pagination for management pages |
| Feature cache | Shared temporary filename can race across processes | Unique temporary files with atomic replace |
| Admin | Missing providers, CMS, settings, security, health and backups | Protected control-center sections with audited mutations |
| Account workflow | Missing reminders, alerts, notifications and job-specific resume comparison | Owner-scoped records, explicit scheduler command, resume evidence comparison |
| Analytics | Only query text stored; currency mixing would mislead charts | Source/location/result counts and currency-aware salary charts |
| Content | Demo-only copy, no About page | Explicit real/demo labels, honest fallbacks, college/developer credits |
| Operations | No SMTP/dev mail adapter or production configuration checks | Private development mail files, SMTP integration, safe structured logs and deployment guidance |

## Route inventory at baseline

Public: `/`, `/register`, `/login`, `/admin/login`, `/logout`, `/jobs`, `/jobs/<id>`, `/methodology`, `/health`.

Candidate: `/dashboard`, `/profile`, `/resume/upload`, `/resume/review/<id>`, `/resume/remove`, `/saved`, `/jobs/<id>/save`, `/jobs/<id>/apply`, `/applications`, `/applications/<id>/status`, `/recommendations`, `/insights`, `/skills`, `/simulator`, `/history`, `/history/snapshot`.

Admin: `/admin/`, `/admin/jobs`, `/admin/jobs/new`, `/admin/jobs/<id>/edit`, `/admin/jobs/<id>/delete`, `/admin/users`.

JSON: `/api/jobs`, `/api/jobs/<id>`, `/api/skills`, `/api/profile`, `/api/recommendations`, `/api/recommend`.

## Integration boundaries

- Backend-only requests to documented provider hosts. No Google/LinkedIn/Indeed scraping.
- Provider credentials remain environment-only; management pages show configuration status, never values.
- External apply links leave JobMatch. Tracking locally never means an application was submitted.
- Adzuna descriptions may be snippets; remote eligibility and unspecified qualifications must not be invented.
- SMTP delivery and actual credentialed provider responses require operator-supplied configuration. Fixture tests are identified separately from live service verification.

Final implementation and validation results are recorded in `UPGRADE_REPORT.md`.
