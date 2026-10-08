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
            features = engine().features_for(sorted(jobs, key=lambda job: job.id))
            print(
                f"Indexed {len(jobs)} active jobs, {features[1].shape[1]} TF-IDF features."
            )
            print(
                f"Local artifact: {Path(app.instance_path) / 'tfidf-cache.npz'} (non-executable; no pickle loading)."
            )
        else:
            print("No active jobs to index.")
