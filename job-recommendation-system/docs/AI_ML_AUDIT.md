# AI/ML repository audit

Audited source baseline: `91c15b5a24db0283a17637b53efd77f3431e43d3`,
2026-10-08. Scope: `job-recommendation-system` and its root GitHub workflow.
The other portfolio projects are outside this upgrade.

## Existing architecture

The Flask application factory in `app.py` registers authentication, candidate,
jobs, recommendations, workspace, public and admin/control blueprints. Models in
`models/database.py` contain users, normalized skills, jobs/provider identities,
saved jobs, local applications, resume drafts, immutable recommendation runs,
notifications/alerts, sessions, rate limits, audit events and settings. SQLite has
foreign-key enforcement and an additive schema upgrader with integrity-checked
backups. Services handle cleaning/seeding, cached provider ingestion, ranking,
analytics, mail and security. Jinja templates and bundled JS/CSS/fonts/Chart.js
provide the responsive UI; there is no need for a frontend framework.

Baseline verification: **167 tests passed** before implementation.

## Existing ML pipeline

Synthetic/local jobs or provider records → cleaning and skill aliases → job-only
TF-IDF and role-family vectors → cosine similarities → seven hand-weighted
factors → deterministic ordering → immutable snapshots. The field called
`semantic` actually holds TF-IDF lexical similarity. Nothing in that baseline
learns ranking weights from relevance judgments. Resume extraction uses bounded
PDF/DOCX text parsing, dictionary patterns, section headings and explicit years;
users review a draft before saving it.

## Findings and priorities

| Priority | Finding | Upgrade / remaining limit |
|---|---|---|
| P0 | Persistent TF-IDF cache deserializes `joblib` objects | Replace with checked NPZ numeric arrays and JSON vocabularies; ignore old pickle files |
| P0 | No dedicated execution boundary around upload parsing | Add a subprocess timeout and Linux CPU/address-space bounds; Windows has timeout and existing document bounds |
| P0 | Raw resume text can place names/contact/sensitive information into text similarity | Rank from allowlisted professional fields; exclude raw resume/name/contact fields, remove explicit sensitive lines |
| P1 | “Semantic” naming overstates a lexical baseline | Preserve the baseline API but label it accurately; separate `tfidf` and actual optional embedding scores |
| P1 | No independent relevance dataset, supervised ranker or held-out comparison | Versioned snapshots, explicit synthetic provenance, group/temporal split, logistic and forest rankers, honest reports |
| P1 | Existing evaluation has only four role-family scenarios and treats weak matches as relevant | Retain its smoke test; add graded 0–3 judgments and report a distinct >=2 relevance threshold |
| P1 | Saved jobs/views/applications do not personalize ranking | Timestamped immutable feedback and a bounded behavior profile with cold-start thresholds |
| P1 | Skill gaps do not expose partial proficiency or dependencies | Add partial matches, per-role/job gaps and ordered prerequisite paths |
| P1 | Resume section extraction provides no review confidence/evidence inventory | Add dictionary/section confidence, tools/domains and a transparent quality checklist |
| P1 | Model/feature versions are insufficient for a trained ranker | JSON metadata, dependency checks, frozen training vocabularies and content digests |
| P2 | Admin analytics lack model comparison and feature importance | Add authenticated `/admin/ml-lab` with actual application counts and separately labeled evaluation data |
| P2 | No recorded A/B assignment/exposure framework | Explicit operator-created experiments, deterministic saved assignments, display exposures and attributed actions |
| P2 | Repeated ORM access could grow into per-job behavior queries | Eager-load history, cap windows, reuse vector caches and aggregate experiment attribution in SQL |

## Security and frontend review

Keep existing scrypt password hashing, revocable hashed sessions, generic recovery
responses, single-use hashed tokens, admin checks, CSRF, shared rate limits, owner
scoping, trusted production origin, encrypted mail requirements, upload extension/
signature/ZIP-expansion bounds, safe URL checks, provider time/size bounds and
credential-free logging. Provider keys remain server-side. Existing templates use
autoescaping and JS uses text nodes for tags. New feedback posts inherit CSRF and
authentication; there is no web model upload or training endpoint. Existing route,
resume, migration, provider, account and UI workflows remain regression-tested.

## Risks that remain

The committed catalogue and new judgments are fictional. They cannot prove hiring
quality, real market demand, subgroup fairness, multilingual skill extraction or
deployment scalability. A pretrained English embedding model is optional and was
not downloaded or benchmarked in this validation environment. Free-text project/
certification descriptions and location/education preferences can still contain
proxies or user-entered personal information. A feature allowlist is a mitigation,
not a fairness certificate. Real labels, consent/retention operations, external
provider credentials and target-machine performance need independent validation.
