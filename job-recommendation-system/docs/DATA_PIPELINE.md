# Data pipeline and reproducible commands

Run all commands from `job-recommendation-system` with Python 3.11 or 3.12.

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m ml.evaluation.evaluate_models --dataset data/relevance_demo.jsonl
python scripts/train_ranker.py --dataset data/relevance_demo.jsonl --model logistic
```

Training on the committed fixture is a teaching exercise. Its output stays
disabled in normal inference. To inspect it locally, explicitly set both
`ALLOW_SYNTHETIC_RANKER=true` and `ML_STRATEGY=ltr`, then restart. For actual model
selection, replace the fixture with separately reviewed real snapshots.

## Ingestion, preprocessing and feature engineering

Provider and local-job ingestion retain the existing cleaning and security services.
The evaluation loader also calls `clean_job_rows`; it does not introduce a second
job normalization implementation. Skill aliases preserve concrete tools (for example
PostgreSQL) while recognizing their broader SQL family. Reviewed professional
fields supply candidate text; raw resume identity text is excluded from ranking.
The numeric contract is:

`skills, tfidf, semantic, role, experience, education, location, salary,
employment, remote, freshness, behavior, semantic_available`.

Score features are divided by 100. Missing semantic similarity becomes 0 with a
separate availability indicator, never a fabricated embedding score. All values
must be finite and in [0,1]. Labels, names, emails, candidate/job IDs and protected
attributes cannot be columns of this feature matrix.

## Relevance snapshot schema

One JSONL row represents one candidate snapshot × job snapshot judgment:

| Field | Meaning |
|---|---|
| `schema_version` | `relevance-v1` |
| `dataset_kind` | `synthetic`, `manual` or `behavioral`, evaluated separately |
| `candidate_id`, `job_id` | Pseudonymous snapshot identifiers, not input features |
| `candidate_features` | Allowlisted profile fields, including skills/role/experience/preferences |
| `job_features` | Existing cleaner input fields/posting date, synthetic flag, currency/pay period, experience-known and remote/source flags |
| `snapshot_at` | Timezone-aware prediction-time snapshot |
| `relevance_label` | 0 irrelevant; 1 weak; 2 relevant; 3 highly relevant |
| `judged_at`, `judgment_method` | Provenance and time the target label became available; `judged_at` is required for behavioral data |
| `behavior_cutoff` | Required for behavioral snapshots; no later than prediction time |

Skill/semantic/role/experience/education/location/salary match columns are derived
at feature generation time, not accepted from reviewers as trusted model inputs.
The committed fixture has 12 fictional profiles, 20 distinct duty-based jobs and
an explicit 240-cell ordinal judgment table. Labels are authored independently
of score functions. They are **synthetic**, even though their table is hand authored.
They are not independent expert review or real behavioral evaluation.

To prepare independent judgments without revealing predictions:

```bash
python scripts/export_relevance_template.py --max-candidates 20 --max-jobs 20
```

This creates a private `instance/ml/relevance-review-template.jsonl` with null
labels. A reviewer supplies every judgment and its provenance/date. Null labels
are rejected. The exporter marks any partition containing demo jobs as synthetic;
the loader refuses fixture jobs labeled as manual/behavioral data. Inspect personal
information and candidate provenance before sharing and downgrade demo profiles
to synthetic as needed. Never commit user review exports. Provider currency,
pay period and unknown-experience flags survive ingestion; missing real-job
metadata defaults to unknown instead of assuming comparable annual INR.
Each candidate must judge the complete declared evaluation pool: unjudged pairs
are not assumed irrelevant. One incomplete query does not manufacture negatives.

## Leakage protection

Manual/synthetic data uses `GroupShuffleSplit` with seed 2026, 75% train / 25% test,
grouped by candidate snapshot. No candidate snapshot appears in both. The fixture
tests unseen candidates against a **known catalogue**, not unseen job templates.
TF-IDF/role vocabularies and IDF are fitted only on training job snapshots.
The ranker stores those vocabularies for inference. Test labels never enter
feature generation or training; held-out metrics are attached after prediction.

Behavioral splits normalize all offsets to UTC, use snapshot time and require training label availability before
the test window, and validate the behavior cutoff. Historical online feedback
uses only events before its cutoff, with no future actions. Offline exported
snapshot training currently disables behavioral features rather than reconstruct
unverified historical events. A fully validated temporal event dataset is future
work; current activity is not represented as a real-world evaluation.

## Persistence and inference

Operator-trained models are portable JSON, not pickle. Metadata includes model
name/type/version, training date, dataset SHA-256/provenance, feature contract,
dependency versions, metrics and hyperparameters. Vocabularies and numeric tree/
coefficient data are validated; incompatible or corrupt artifacts cannot silently
execute. Atomic writes preserve the previous file until a complete replacement.
Digests detect accidental modifications; they are not an authenticity signature.
Only operator-managed private files are loaded, with no model-upload endpoint.
