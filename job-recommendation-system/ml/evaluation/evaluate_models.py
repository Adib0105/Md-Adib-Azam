"""Run: python -m ml.evaluation.evaluate_models --dataset data/relevance_demo.jsonl"""

import argparse
import json
import tempfile
from collections import Counter
from datetime import date
from pathlib import Path
from statistics import mean
from app import create_app
from config import ROOT
from ml import PIPELINE_VERSION, FEATURE_VERSION
from ml.features.schema import feature_matrix
from ml.features.representation import serialize_representation
from ml.models.rankers import train_ranker, dependency_versions
from ml.pipelines.dataset import (
    load_dataset,
    split_dataset,
    jobs_for,
    validate_complete_judgments,
)
from ml.evaluation.metrics import ranking_metrics
from services.recommendation_service import engine


def scored_queries(records, jobs, features):
    output = {}
    for identity in sorted({r["candidate_id"] for r in records}):
        pairs = [r for r in records if r["candidate_id"] == identity]
        local_jobs = [jobs[r["job_id"]] for r in pairs]
        as_of = date.fromisoformat(pairs[0]["snapshot_at"][:10])
        rows = engine().rank(
            pairs[0]["candidate_features"],
            local_jobs,
            strategy="hybrid",
            fixed_features=features,
            as_of=as_of,
        )
        numeric_to_id = {jobs[r["job_id"]].id: r["job_id"] for r in pairs}
        output[identity] = {
            "rows": rows,
            "job_ids": [numeric_to_id[r["job"].id] for r in rows],
            "judgments": {r["job_id"]: r["relevance_label"] for r in pairs},
        }
    return output


def macro(queries, score_key=None, predictor=None):
    results = []
    for identity, query in queries.items():
        if predictor:
            scores = predictor.predict(feature_matrix(query["rows"])).tolist()
        else:
            scores = [
                (
                    r["baseline_score"]
                    if score_key == "weighted"
                    else r["score"] if score_key == "hybrid" else r["scores"][score_key]
                )
                for r in query["rows"]
            ]
        ranked = [
            job
            for job, _ in sorted(
                zip(query["job_ids"], scores), key=lambda p: (-p[1], p[0])
            )
        ]
        results.append(
            {
                "candidate_id": identity,
                **ranking_metrics(ranked, query["judgments"]),
                "top_job_ids": ranked[:5],
            }
        )
    keys = [key for key in results[0] if key not in {"candidate_id", "top_job_ids"}]
    return {key: round(mean(row[key] for row in results), 6) for key in keys}, results


def evaluate(dataset_path, *, app_config=None, artifact_dir=None):
    records, version = load_dataset(dataset_path)
    models = {
        name: {"status": "not_evaluated", "metrics": None}
        for name in [
            "tfidf",
            "weighted",
            "embedding",
            "hybrid",
            "ltr_logistic",
            "ltr_random_forest",
        ]
    }
    report = {
        "report_version": "evaluation-v1",
        "pipeline_version": PIPELINE_VERSION,
        "feature_version": FEATURE_VERSION,
        "dataset": {
            "version": version,
            "kind": records[0]["dataset_kind"] if records else "unknown",
            "samples": len(records),
            "candidates": len({r["candidate_id"] for r in records}),
            "jobs": len({r["job_id"] for r in records}),
            "label_counts": dict(Counter(r["relevance_label"] for r in records)),
        },
        "dependency_versions": dependency_versions(),
        "ks": [5, 10, 20],
        "relevance_threshold": 2,
        "models": models,
        "best_model": None,
        "best_model_on_fixture": None,
        "limitations": [
            "No real-world hiring accuracy, ATS score or placement prediction is measured.",
            "A pointwise ordinal classifier/regressor is experimental learning-to-rank, not pairwise or listwise training.",
            "Unjudged pairs are excluded, never manufactured as negative labels.",
            "Binary relevance uses labels >=2; graded NDCG uses 0–3 labels. Precision@K divides by K even when fewer jobs are returned.",
        ],
    }
    try:
        validate_complete_judgments(records)
        train, test, methodology = split_dataset(records)
    except ValueError as error:
        report.update(status="insufficient_data", methodology=str(error))
        report["limitations"].append(str(error))
        return report
    report["methodology"] = methodology
    report["dataset"].update(
        training_samples=len(train),
        evaluation_samples=len(test),
        training_candidates=len({r["candidate_id"] for r in train}),
        evaluation_candidates=len({r["candidate_id"] for r in test}),
        training_candidate_ids=sorted({r["candidate_id"] for r in train}),
        evaluation_candidate_ids=sorted({r["candidate_id"] for r in test}),
    )
    with tempfile.TemporaryDirectory() as directory:
        config = {
            "TESTING": True,
            "SECRET_KEY": "offline-evaluation-only",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "INSTANCE_PATH": str(Path(directory) / "instance"),
            "SEED_ON_START": False,
            "MODEL_CACHE": False,
            "TEST_PASSWORD_HASH_METHOD": "pbkdf2:sha256:1000",
            **(app_config or {}),
        }
        application = create_app(config)
        with application.app_context():
            train_jobs = jobs_for(train)
            # Fitting only the training corpus prevents vocabulary/IDF leakage.
            features = engine().features_for(
                sorted(train_jobs.values(), key=lambda j: j.id)
            )
            all_jobs = jobs_for(records)
            train_queries = scored_queries(train, all_jobs, features)
            test_queries = scored_queries(test, all_jobs, features)
            matrix = feature_matrix(
                [row for query in train_queries.values() for row in query["rows"]]
            )
            labels = [
                query["judgments"][job]
                for query in train_queries.values()
                for job in query["job_ids"]
            ]
            for name, key in [
                ("tfidf", "tfidf"),
                ("weighted", "weighted"),
                ("hybrid", "hybrid"),
            ]:
                scores, queries = macro(test_queries, score_key=key)
                models[name] = {
                    "status": "evaluated",
                    "version": (
                        "tfidf-lexical-v2"
                        if name == "tfidf"
                        else (
                            "seven-factor-v2"
                            if name == "weighted"
                            else PIPELINE_VERSION
                        )
                    ),
                    "metrics": scores,
                    "queries": queries,
                }
            if all(
                row["scores"]["semantic"] is not None
                for query in test_queries.values()
                for row in query["rows"]
            ):
                scores, queries = macro(test_queries, score_key="semantic")
                models["embedding"] = {
                    "status": "evaluated",
                    "version": application.extensions["embedding_service"].version,
                    "metrics": scores,
                    "queries": queries,
                }
            else:
                models["embedding"] = {
                    "status": "unavailable",
                    "reason": application.extensions["embedding_service"].reason,
                    "metrics": None,
                }
            for kind in ["logistic", "random_forest"]:
                try:
                    representation = serialize_representation(
                        features,
                        (
                            application.extensions["embedding_service"].version
                            if application.extensions["embedding_service"].encoder
                            is not None
                            else None
                        ),
                    )
                    ranker = train_ranker(
                        matrix,
                        labels,
                        kind,
                        dataset_version=version,
                        dataset_kind=report["dataset"]["kind"],
                        representation=representation,
                    )
                    scores, queries = macro(test_queries, predictor=ranker)
                    ranker.set_metrics(
                        {
                            "held_out": scores,
                            "evaluation_samples": len(test),
                            "methodology": methodology,
                        }
                    )
                    models["ltr_" + kind] = {
                        "status": "evaluated",
                        "metrics": scores,
                        "queries": queries,
                        "metadata": ranker.metadata,
                    }
                    if artifact_dir:
                        ranker.save(Path(artifact_dir) / (kind + ".json"))
                except ValueError as error:
                    models["ltr_" + kind] = {
                        "status": "insufficient_training_data",
                        "reason": str(error),
                        "metrics": None,
                    }
            report["embedding_backend"] = application.extensions[
                "embedding_service"
            ].status()
    available = {
        name: result
        for name, result in models.items()
        if result["status"] == "evaluated"
    }
    best = (
        sorted(
            available, key=lambda name: (-available[name]["metrics"]["ndcg@10"], name)
        )[0]
        if available
        else None
    )
    if report["dataset"]["kind"] == "synthetic":
        report["best_model_on_fixture"] = best
        report["limitations"].append(
            "Fictional author-created labels and narrow scenarios can favor title/skill matching. They are not independent human judgments or real behavioral evidence. No model is selected for production from this fixture."
        )
    else:
        report["best_model"] = best
    report["status"] = "evaluated_with_limitations"
    if report["dataset"]["evaluation_candidates"] < 20:
        report["limitations"].append(
            "Fewer than 20 held-out candidates: estimates are unstable; collect a larger independent reviewed dataset before choosing a model."
        )
    return report


def write_reports(report, destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "model_evaluation.json").write_text(
        json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    dataset = report["dataset"]
    lines = [
        "# Model evaluation",
        "",
        f"Status: **{report['status']}**. Dataset kind: **{dataset['kind']}**.",
        "",
        f"{dataset['samples']} judgments; {dataset['candidates']} candidates; {dataset['jobs']} jobs. Training: {dataset.get('training_samples', 0)} pairs; held out: {dataset.get('evaluation_samples', 0)} pairs.",
        "",
        report["methodology"],
        "",
        "Labels: 0 irrelevant, 1 weak, 2 relevant, 3 highly relevant. Binary relevance is >=2. NDCG uses graded gains. MAP and MRR use the entire judged ranking. Candidate metrics are macro averaged.",
        "",
        "| Model | Status | Precision@5 | Precision@10 | Recall@5 | Recall@10 | NDCG@5 | NDCG@10 | MRR | MAP |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, result in report["models"].items():
        metrics = result.get("metrics") or {}
        values = [
            f"{metrics[key]:.4f}" if key in metrics else "Unavailable"
            for key in [
                "precision@5",
                "precision@10",
                "recall@5",
                "recall@10",
                "ndcg@5",
                "ndcg@10",
                "mrr",
                "map",
            ]
        ]
        lines.append(f"| {name} | {result['status']} | " + " | ".join(values) + " |")
    lines += [
        "",
        "## Top-K comparison",
        "",
        "| Model | K | Precision | Recall | NDCG | MRR (full ranking) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, result in report["models"].items():
        metrics = result.get("metrics")
        if metrics:
            for k in [5, 10, 20]:
                lines.append(
                    f"| {name} | {k} | {metrics[f'precision@{k}']:.4f} | {metrics[f'recall@{k}']:.4f} | {metrics[f'ndcg@{k}']:.4f} | {metrics['mrr']:.4f} |"
                )
    lines += [
        "",
        f"Highest NDCG@10 on the synthetic fixture: **{report.get('best_model_on_fixture') or 'not applicable'}**. This is not a production model selection.",
        "",
        "## Limitations",
        "",
    ] + ["- " + value for value in report["limitations"]]
    lines += [
        "",
        "Model versions, feature contract, dataset SHA-256, dependency versions, per-candidate metrics and train/test IDs are recorded in `model_evaluation.json`. The original synthetic smoke evaluation remains available as `scripts/evaluate_model.py`; its weak-label binary threshold differs, so its metrics should not be compared directly.",
        "",
    ]
    (destination / "MODEL_EVALUATION.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset", type=Path, default=ROOT / "data/relevance_demo.jsonl"
    )
    parser.add_argument("--output", type=Path, default=ROOT / "docs")
    parser.add_argument("--artifacts", type=Path)
    args = parser.parse_args()
    report = evaluate(args.dataset, artifact_dir=args.artifacts)
    write_reports(report, args.output)
    print(
        json.dumps(
            {
                "status": report["status"],
                "dataset": report["dataset"],
                "best_on_synthetic_fixture": report["best_model_on_fixture"],
                "reports": str(args.output),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
