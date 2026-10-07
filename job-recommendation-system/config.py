"""Local-first settings. All recommendation weights live here."""

import os
from datetime import timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RECOMMENDATION_WEIGHTS = {
    "skills": 0.35,
    "semantic": 0.25,
    "experience": 0.15,
    "education": 0.10,
    "location": 0.05,
    "salary": 0.05,
    "role": 0.05,
}


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///job_recommendation.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    MAX_FORM_MEMORY_SIZE = 256 * 1024
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("APP_ENV") == "production"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    WTF_CSRF_TIME_LIMIT = 8 * 60 * 60
    SEED_ON_START = True
    RECOMMENDATION_WEIGHTS = RECOMMENDATION_WEIGHTS
    MODEL_CACHE = True
    TESTING = False


def validate_weights(weights):
    if set(weights) != set(RECOMMENDATION_WEIGHTS):
        raise ValueError("Provide exactly the seven documented score weights.")
    if any(
        not isinstance(w, (float, int)) or not 0 <= w <= 1 for w in weights.values()
    ):
        raise ValueError("Weights must be finite values from 0 to 1.")
    if abs(sum(weights.values()) - 1) > 1e-9:
        raise ValueError("Recommendation weights must sum to 1.")
