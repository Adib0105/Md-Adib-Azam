# Validation record

Validation performed on **7 October 2026**. The tested runtime was Linux, Python 3.12 and headless Chromium 134.0.6998.35. Windows PowerShell instructions and Windows/Linux GitHub Actions configuration are included; a physical Windows PC and a GitHub Actions run were **not** exercised in this session.

## Installation and automated checks

- Created a new virtual environment without access to system site packages.
- Installed the exact `requirements-dev.txt` dependency set successfully.
- Ran **60 automated tests**, all passing.
- Ran Ruff Python formatting and unused/undefined-name checks; no remaining `F` diagnostics.
- Checked JavaScript syntax with Node.
- Created and seeded 640 jobs with zero invalid-row errors.
- Verified idempotent seeding, durable SQLite data after application recreation, and cached model loading.
- Measured seven full ranking calls over 640 jobs. The median of six warm calls was approximately **117 ms** on this execution environment. This is a local sample, not a performance guarantee for other computers. No TF-IDF refit was needed after the existing artifact loaded.

## Browser workflow

The browser test passed this sequence with actual form submissions and active CSRF protection:

1. Open landing page, candidate login, dashboard and job explanation.
2. Render all eight Career Insights charts.
3. Register a fresh candidate; edit and save their profile with skill tags.
4. Upload a DOCX, inspect/edit its review draft, and confirm the extracted fields.
5. Open ranked recommendations; save a job; add it to the local application tracker.
6. Update the tracker status to Interview.
7. Simulate Tableau + DAX and render twelve before/after results.
8. Inspect recommendation history; log out.
9. Sign in through the separate administrator page; add, edit and remove a job.

The run recorded **zero JavaScript errors, zero failed HTTP resources and zero external network requests**. Non-local HTTP requests were blocked by the test browser, verifying that the application's normal UI does not require a CDN or external API.

After the visual update, the full browser workflow was repeated successfully. The browser loaded bundled **Manrope and Fraunces** fonts, observed the normal-motion entrances, and verified that switching to reduced motion stops them while leaving the primary action usable. The landing page also remained usable with JavaScript disabled. Landing-page widths of **1024, 768 and 390 pixels** showed no horizontal overflow. The GitHub banner contains 48 animation frames and plays a single four-second cycle.

Dashboard widths of **1366, 1024, 768 and 390 pixels** had no document-level horizontal overflow. Jobs, profile, skill analysis, simulator, insights, applications and history were also checked at 390 pixels. Tables scroll inside their own containers when needed. Representative desktop/mobile screenshots were inspected for layout.

Machine-readable browser evidence is in `screenshots/browser-results.json`. The optional browser test is `tests/browser_smoke.cjs`; it requires Node + Playwright and a **disposable** local instance with explicitly seeded demo accounts. Set `RESUME_FIXTURE` to a sample DOCX/PDF to exercise upload/review. Do not run it against an instance containing important personal data: it creates test candidates and test jobs.

## Coverage boundaries

The tests exercise registration/login/session protection, CSRF token rotation, admin isolation, owner-scoped applications/resume drafts, aliases/token boundaries, salary/experience/education/location scoring, sorting/filtering/pagination, consistent explanations, feature-cache reuse and invalidation, snapshot deduplication, simulator immutability, valid PDF/DOCX extraction, scanned/corrupt/oversized/expanded-archive rejection, admin CRUD, expired-job exclusion and persistence.

This is not a penetration test, independent accessibility audit, load test, physical Windows verification, or validation against real recruitment outcomes. The app is intended to run on loopback. Production hosting and hostile document processing need additional controls documented in the README.

## Synthetic evaluation

`evaluation.json` contains Precision@10, Recall@10 and NDCG@10 over four authored candidate scenarios and 640 generated jobs. Macro averages in this synthetic smoke run were:

| Metric | Result |
| --- | ---: |
| Precision@10 | 1.0000 |
| Recall@10 | 0.1175 |
| NDCG@10 | 0.9804 |

These favorable precision/NDCG values reflect an intentionally easy, template-based role-family proxy. There are no real hiring labels, independently judged candidate/job pairs or held-out real-world population. They do not establish production recommendation quality, fairness, calibration or employment success.
