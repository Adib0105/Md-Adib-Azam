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

HYBRID_WEIGHTS = {
    "skills": 0.30,
    "tfidf": 0.19,
    "semantic": 0.14,
    "experience": 0.12,
    "education": 0.08,
    "location": 0.05,
    "salary": 0.04,
    "role": 0.035,
    "employment": 0.015,
    "remote": 0.015,
    "freshness": 0.015,
    "behavior": 0.0,
}


class Config:
    APP_ENV = os.getenv("APP_ENV", "development")
    APP_BASE_URL = os.getenv("APP_BASE_URL", "http://127.0.0.1:5000").rstrip("/")
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
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    SESSION_HOURS = 8
    SESSION_IDLE_MINUTES = int(os.getenv("SESSION_IDLE_MINUTES", "60"))
    REMEMBER_DAYS = int(os.getenv("REMEMBER_DAYS", "30"))
    RESET_TOKEN_MINUTES = 30
    AUTO_UPGRADE_SCHEMA = (
        os.getenv(
            "AUTO_UPGRADE_SCHEMA", "true" if APP_ENV != "production" else "false"
        ).lower()
        == "true"
    )
    WTF_CSRF_TIME_LIMIT = 8 * 60 * 60
    SEED_ON_START = True
    RECOMMENDATION_WEIGHTS = RECOMMENDATION_WEIGHTS
    MODEL_CACHE = True
    ML_STRATEGY = os.getenv("ML_STRATEGY", "hybrid")
    HYBRID_WEIGHTS = HYBRID_WEIGHTS
    EMBEDDINGS_ENABLED = os.getenv("EMBEDDINGS_ENABLED", "false").lower() == "true"
    EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_MODEL_PATH = os.getenv("EMBEDDING_MODEL_PATH", "")
    EMBEDDING_MODEL_REVISION = os.getenv("EMBEDDING_MODEL_REVISION", "unprepared")
    EMBEDDING_DIMENSION = 384
    EMBEDDING_BATCH_SIZE = 32
    BEHAVIOR_MIN_JOBS = 5
    BEHAVIOR_MIN_ACTIONS = 3
    BEHAVIOR_MAX_WEIGHT = 0.10
    ALLOW_SYNTHETIC_RANKER = (
        os.getenv("ALLOW_SYNTHETIC_RANKER", "false").lower() == "true"
    )
    ML_EXPERIMENT = os.getenv("ML_EXPERIMENT", "")
    RESUME_PARSE_TIMEOUT = 15
    TESTING = False
    TEST_PASSWORD_HASH_METHOD = None
    ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "")
    ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "")
    USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY", "")
    USAJOBS_USER_AGENT = os.getenv("USAJOBS_USER_AGENT", "")
    ENABLE_ADZUNA = os.getenv("ENABLE_ADZUNA", "true").lower() == "true"
    ENABLE_USAJOBS = os.getenv("ENABLE_USAJOBS", "false").lower() == "true"
    REAL_JOB_CACHE_TTL_MINUTES = int(os.getenv("REAL_JOB_CACHE_TTL_MINUTES", "30"))
    EXTERNAL_JOB_STALE_DAYS = int(os.getenv("EXTERNAL_JOB_STALE_DAYS", "14"))
    EXTERNAL_JOB_MAX_AGE_DAYS = int(os.getenv("EXTERNAL_JOB_MAX_AGE_DAYS", "60"))
    PROVIDER_TIMEOUT_SECONDS = 8
    PROVIDER_MAX_RESPONSE_BYTES = 2 * 1024 * 1024
    PROVIDER_REQUESTS_PER_HOUR = int(os.getenv("PROVIDER_REQUESTS_PER_HOUR", "60"))
    MAX_RANKING_JOBS = int(os.getenv("MAX_RANKING_JOBS", "2000"))
    MAIL_BACKEND = os.getenv(
        "MAIL_BACKEND", "disabled" if APP_ENV == "production" else "file"
    )
    MAIL_SERVER = os.getenv("MAIL_SERVER", "")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "jobmatch@localhost")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_ASYNC = True
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def validate_weights(weights):
    if set(weights) != set(RECOMMENDATION_WEIGHTS):
        raise ValueError("Provide exactly the seven documented score weights.")
    if any(
        not isinstance(w, (float, int)) or not 0 <= w <= 1 for w in weights.values()
    ):
        raise ValueError("Weights must be finite values from 0 to 1.")
    if abs(sum(weights.values()) - 1) > 1e-9:
        raise ValueError("Recommendation weights must sum to 1.")


def validate_ml_config(config):
    import math

    values = config["HYBRID_WEIGHTS"]
    if (
        set(values) != set(HYBRID_WEIGHTS)
        or any(
            isinstance(w, bool)
            or not isinstance(w, (int, float))
            or not math.isfinite(w)
            or not 0 <= w <= 1
            for w in values.values()
        )
        or abs(sum(values.values()) - 1) > 1e-9
    ):
        raise ValueError(
            "Hybrid weights must match the feature contract and sum to one."
        )
    if values["behavior"] != 0:
        raise ValueError(
            "Behavior starts at zero; only sufficient history enables its bounded adjustment."
        )
    if config["ML_STRATEGY"] not in {"weighted", "hybrid", "ltr"}:
        raise ValueError("ML_STRATEGY must be weighted, hybrid or ltr.")
    if (
        not 0 <= config["BEHAVIOR_MAX_WEIGHT"] <= 0.10
        or config["BEHAVIOR_MIN_JOBS"] < 5
        or config["BEHAVIOR_MIN_ACTIONS"] < 3
    ):
        raise ValueError(
            "Personalization requires five jobs, three meaningful actions, and at most 10% weight."
        )
    if not 1 <= config["EMBEDDING_BATCH_SIZE"] <= 128:
        raise ValueError("Embedding batch size must be 1–128.")
