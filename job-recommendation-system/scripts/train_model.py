"""Fit TF-IDF on job text only; this is unsupervised feature extraction, not LLM training."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from services.recommendation_service import active_jobs, engine

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        jobs = active_jobs()
        if jobs:
            features = engine().features_for(jobs)
            print(
                f"Indexed {len(jobs)} active jobs, {features[1].shape[1]} TF-IDF features."
            )
            print(
                "Local artifact: instance/model.joblib (do not share or load untrusted model files)."
            )
        else:
            print("No active jobs to index.")
