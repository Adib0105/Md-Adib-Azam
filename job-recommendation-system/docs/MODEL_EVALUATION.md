# Model evaluation

Status: **evaluated_with_limitations**. Dataset kind: **synthetic**.

240 judgments; 12 candidates; 20 jobs. Training: 180 pairs; held out: 60 pairs.

Candidate-group held-out 75/25 split (seed 2026); disjoint candidate snapshots, known job catalogue. TF-IDF/role vocabularies fitted only on training job snapshots.

Labels: 0 irrelevant, 1 weak, 2 relevant, 3 highly relevant. Binary relevance is >=2. NDCG uses graded gains. MAP and MRR use the entire judged ranking. Candidate metrics are macro averaged.

| Model | Status | Precision@5 | Precision@10 | Recall@5 | Recall@10 | NDCG@5 | NDCG@10 | MRR | MAP |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tfidf | evaluated | 0.5333 | 0.2667 | 1.0000 | 1.0000 | 0.9349 | 0.9402 | 1.0000 | 1.0000 |
| weighted | evaluated | 0.5333 | 0.2667 | 1.0000 | 1.0000 | 0.9432 | 0.9451 | 1.0000 | 1.0000 |
| embedding | unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable |
| hybrid | evaluated | 0.5333 | 0.2667 | 1.0000 | 1.0000 | 0.9631 | 0.9479 | 1.0000 | 1.0000 |
| ltr_logistic | evaluated | 0.5333 | 0.2667 | 1.0000 | 1.0000 | 0.9631 | 0.9623 | 1.0000 | 1.0000 |
| ltr_random_forest | evaluated | 0.4667 | 0.2667 | 0.8889 | 1.0000 | 0.9388 | 0.9462 | 1.0000 | 0.9444 |

## Top-K comparison

| Model | K | Precision | Recall | NDCG | MRR (full ranking) |
|---|---:|---:|---:|---:|---:|
| tfidf | 5 | 0.5333 | 1.0000 | 0.9349 | 1.0000 |
| tfidf | 10 | 0.2667 | 1.0000 | 0.9402 | 1.0000 |
| tfidf | 20 | 0.1333 | 1.0000 | 0.9743 | 1.0000 |
| weighted | 5 | 0.5333 | 1.0000 | 0.9432 | 1.0000 |
| weighted | 10 | 0.2667 | 1.0000 | 0.9451 | 1.0000 |
| weighted | 20 | 0.1333 | 1.0000 | 0.9798 | 1.0000 |
| hybrid | 5 | 0.5333 | 1.0000 | 0.9631 | 1.0000 |
| hybrid | 10 | 0.2667 | 1.0000 | 0.9479 | 1.0000 |
| hybrid | 20 | 0.1333 | 1.0000 | 0.9826 | 1.0000 |
| ltr_logistic | 5 | 0.5333 | 1.0000 | 0.9631 | 1.0000 |
| ltr_logistic | 10 | 0.2667 | 1.0000 | 0.9623 | 1.0000 |
| ltr_logistic | 20 | 0.1333 | 1.0000 | 0.9862 | 1.0000 |
| ltr_random_forest | 5 | 0.4667 | 0.8889 | 0.9388 | 1.0000 |
| ltr_random_forest | 10 | 0.2667 | 1.0000 | 0.9462 | 1.0000 |
| ltr_random_forest | 20 | 0.1333 | 1.0000 | 0.9768 | 1.0000 |

Highest NDCG@10 on the synthetic fixture: **ltr_logistic**. This is not a production model selection.

## Limitations

- No real-world hiring accuracy, ATS score or placement prediction is measured.
- A pointwise ordinal classifier/regressor is experimental learning-to-rank, not pairwise or listwise training.
- Unjudged pairs are excluded, never manufactured as negative labels.
- Binary relevance uses labels >=2; graded NDCG uses 0–3 labels. Precision@K divides by K even when fewer jobs are returned.
- Fictional author-created labels and narrow scenarios can favor title/skill matching. They are not independent human judgments or real behavioral evidence. No model is selected for production from this fixture.
- Fewer than 20 held-out candidates: estimates are unstable; collect a larger independent reviewed dataset before choosing a model.

Model versions, feature contract, dataset SHA-256, dependency versions, per-candidate metrics and train/test IDs are recorded in `model_evaluation.json`. The original synthetic smoke evaluation remains available as `scripts/evaluate_model.py`; its weak-label binary threshold differs, so its metrics should not be compared directly.
