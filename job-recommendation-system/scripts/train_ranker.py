"""Explicit offline training; production activation is an operator decision."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from ml.pipelines.dataset import (
    load_dataset,
    split_dataset,
    jobs_for,
    validate_complete_judgments,
)
from ml.evaluation.evaluate_models import scored_queries
from ml.features.schema import feature_matrix
from ml.models.rankers import train_ranker
from ml.features.representation import serialize_representation
from services.recommendation_service import engine


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True, type=Path)
    parser.add_argument(
        "--model", choices=["logistic", "random_forest"], default="logistic"
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    records, version = load_dataset(args.dataset)
    validate_complete_judgments(records)
    training, _, methodology = split_dataset(records)
    app = create_app()
    with app.app_context():
        training_jobs = jobs_for(training)
        features = engine().features_for(
            sorted(training_jobs.values(), key=lambda j: j.id)
        )
        queries = scored_queries(training, training_jobs, features)
        matrix = feature_matrix(
            [row for query in queries.values() for row in query["rows"]]
        )
        labels = [
            query["judgments"][identity]
            for query in queries.values()
            for identity in query["job_ids"]
        ]
        ranker = train_ranker(
            matrix,
            labels,
            args.model,
            dataset_version=version,
            dataset_kind=records[0]["dataset_kind"],
            metrics={
                "methodology": methodology,
                "evaluation": "Run the held-out evaluation separately; no training metrics substituted.",
            },
            representation=serialize_representation(
                features,
                (
                    app.extensions["embedding_service"].version
                    if app.extensions["embedding_service"].encoder is not None
                    else None
                ),
            ),
        )
        output = args.output or Path(app.instance_path) / "ml" / "ranker.json"
        ranker.save(output)
    print(
        f"Saved {args.model} trained on {len(training)} {records[0]['dataset_kind']} judgments to {output}. Set ML_STRATEGY=ltr to request it. Synthetic models stay disabled unless ALLOW_SYNTHETIC_RANKER=true is explicitly set for a demonstration."
    )


if __name__ == "__main__":
    main()
