# Architecture and data contracts

The application factory registers five blueprints and initializes SQLite before accepting requests. `python app.py` starts Waitress on loopback with four threads; no debug reloader or automatic browser-opening loop is used.

## Persistent entities

| Entity | Relationship and purpose |
| --- | --- |
| User | Unique lowercase email, password hash, candidate profile, internal admin flag |
| CandidateSkill | Many per user, unique normalized name per owner, self-reported proficiency |
| Job | Source ID, structured job features, synthetic-data flag, active status and view count |
| SavedJob | Unique `(user_id, job_id)` shortlist entry |
| Application | Unique `(user_id, job_id)` local application; user-controlled status |
| RecommendationRun | User, profile summary, model weights, fingerprint, timestamp, reason |
| Recommendation | Up to 50 job score snapshots per run, including title/company and seven component scores |
| ResumeDraft | UUID, owner, parsed fields/text and one-hour access expiration |
| SearchEvent | Local query string and timestamp, aggregated in admin charts |

Foreign keys are enforced and indexes support email, ownership, source/job ID and recent-history lookups. Candidate skill deletion cascades with its owner. Job removal is soft deletion so historical references remain intact. There is no separate admin self-registration route.

## Ranking and state boundaries

1. Job CSV rows are cleaned and seeded once. Admin edits validate the same structured fields.
2. Feature matrices are fitted on job text and role text. A content fingerprint detects model-input changes; profile requests reuse the existing matrices.
3. A candidate's normalized explicit skills are used for skill coverage; education, projects, experience summary, certifications, interests, role and reviewed resume text form the text vector.
4. Seven components produce a weighted score. Explanations and contributions come from those same computed values.
5. List pages recalculate current scores without creating history records. Profile/resume writes and explicit snapshot requests store history. Identical consecutive snapshots are deduplicated.
6. What-if calculations copy profile data and add dictionary skills in memory. They do not call persistence routines.
7. Saved/application routes derive the owner from the signed session, never from a submitted user ID. Resume review queries require both UUID and owner.

## Data and UI honesty

- No score is generated randomly. Randomness is limited to a seeded, explicitly fictional dataset generator.
- TF-IDF is described as lexical similarity, not a pretrained language model.
- Missing user context is distinguishable from zero years of experience.
- Unknown salary/education/experience can contribute a neutral 50 rather than an invented perfect match.
- Completeness labels describe available input data, not validated qualifications or hiring confidence.
- Dataset demand and salary charts carry the synthetic-data caveat, and tables expose their exact underlying values.
- Apply actions write local tracker records. Nothing is sent to employers.

## Extending the project

Add new skill aliases in `models/skill_extractor.py`, role vocabulary in `models/recommendation_model.py`, and state mapping in `utils/constants.py`. Adjust weights in `config.py` and rerun the ranking tests/evaluation. A real job feed should supply authorized data with explicit provenance and replace the fictional-data assumptions. A production migration must add database migrations, deployment hardening and appropriately isolated document processing.
