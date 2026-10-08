# Recommender methodology

## Baseline and hybrid

The retained baseline uses seven configured hand-weighted features. Its historic
`semantic` field remains for API compatibility and means **TF-IDF lexical cosine**.
Hybrid output splits that into `tfidf` and optional actual `semantic` embedding
cosine. Every score is bounded 0–100 and weighted contributions explain the total.
Scores measure compatibility under declared assumptions; they are not calibrated
probabilities, hiring predictions or percentages of employer approval.

| Hybrid factor | Default weight |
|---|---:|
| Required/preferred skill overlap | .300 |
| TF-IDF lexical similarity | .190 |
| Pretrained embedding cosine | .140 |
| Experience fit | .120 |
| Education qualification level | .080 |
| Location fit | .050 |
| Salary fit | .040 |
| Role-family lexical fit | .035 |
| Employment preference | .015 |
| Remote preference | .015 |
| Posting freshness | .015 |
| Behavior | .000 until sufficient history |

Weights live in `config.py`, validated at startup. Missing embeddings remove the
.14 weight and proportionally redistribute the remaining weights. Unknown salary,
experience and incompatible currency/periods keep their conservative neutral fit.
Missing posting time has neutral freshness. A zero-requirement skill gap is
unscored; it is not a perfect match. Existing baseline admin weights remain available.

With at least five distinct interacted jobs and three distinct meaningful-action
jobs, behavior receives at most .10 and other weights are proportionally reduced.
Each action kind/job uses its latest signal with a 90-day decay half-life and a
365-day history window. Repeated views cannot meet meaningful-action thresholds.
Save/apply/interview/offer are positive interest signals; an explicit candidate
rejection/ignore is negative. Employer rejection is neutral, not an inferred dislike.
No interaction is assumed from absence of a click. Weight adjustment reasons and
actual model metadata are exposed in results and saved history.

## Optional semantic representation

`sentence-transformers/all-MiniLM-L6-v2` is a compact pretrained English sentence
encoder with 384-dimensional vectors and a 256-token input limit. Model weights
are prepared once by an operator at a pinned upstream commit, then loaded locally
with remote code disabled and safetensors required. Job vectors are cached by
model revision plus normalized content; unchanged jobs are reused across batches
and restarts. Candidate vectors are kept in the bounded in-process cache, not
written as candidate text. Text is truncated by the encoder, so long resumes or
jobs can lose context; identity text is excluded before inference.

The extension is implemented but genuine model inference/quality was **not**
validated in this environment. Backend contracts/caching/fallbacks use test doubles.
The committed evaluation explicitly records embeddings as unavailable.

## Experimental supervised ranking

Logistic Regression predicts ordinal classes 0–3 and uses their expected value as
ranking utility. Random Forest regression predicts the ordinal label directly.
Both train on the exact same normalized feature schema without label/identity
columns. These are pointwise learning-to-rank baselines, not pairwise/listwise
optimizers. The evaluator compares each ranker's raw utility ranking separately.
The optional web `ltr` mode uses 80% explainable hybrid score + 20% ranker utility.
Thus pure-ranker evaluation numbers must not be presented as the blended live score.
Frozen training TF-IDF features and embedding-version compatibility are enforced.

Global importance is absolute logistic coefficient magnitude or forest impurity
importance. Neither proves causality. Per-result ranker ablations compare utility
with one normalized feature set to zero; correlated features make these effects
non-additive. This is sensitivity analysis, not SHAP or calibrated confidence.

## Career tools and limitations

Skill gaps use exact/self-reported intermediate skills as full credit, related or
beginner skills as half credit, and missing skills as zero. A configurable curated
dependency graph orders prerequisites before the target skill, ending in a portfolio
milestone. Career readiness means skill coverage for catalogue/educational templates,
not promotion likelihood or guaranteed eligibility. Resume Strength is an evidence
checklist; absent experience may be reasonable for a student. Extraction confidences
are transparent heuristic review aids, not verified credentials or probabilities.

Primary references: [Sentence Transformer API](https://www.sbert.net/docs/package_reference/sentence_transformer/model.html),
[model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2),
[scikit-learn persistence guidance](https://scikit-learn.org/stable/model_persistence.html).
