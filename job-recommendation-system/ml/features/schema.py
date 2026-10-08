import math
import numpy as np
from ml import FEATURE_VERSION

FEATURE_NAMES = (
    "skills",
    "tfidf",
    "semantic",
    "role",
    "experience",
    "education",
    "location",
    "salary",
    "employment",
    "remote",
    "freshness",
    "behavior",
    "semantic_available",
)


def feature_vector(scores):
    """Scores are 0–100; features are 0–1. Labels and identities cannot enter X."""
    vector = []
    for name in FEATURE_NAMES:
        value = scores.get(name)
        if name == "semantic_available":
            number = float(scores.get("semantic") is not None)
        else:
            number = 0.0 if value is None else float(value) / 100
        if not math.isfinite(number) or not 0 <= number <= 1:
            raise ValueError(f"Invalid normalized feature: {name}")
        vector.append(number)
    return vector


def feature_matrix(rows):
    return np.asarray(
        [feature_vector(row["scores"]) for row in rows], dtype=float
    ).reshape(-1, len(FEATURE_NAMES))


def validate_matrix(matrix):
    result = np.asarray(matrix, dtype=float)
    if result.ndim != 2 or result.shape[1] != len(FEATURE_NAMES):
        raise ValueError("Incompatible feature matrix.")
    if not np.isfinite(result).all() or (result < 0).any() or (result > 1).any():
        raise ValueError("Features must be finite and normalized to 0–1.")
    return result


def contract():
    return {"feature_version": FEATURE_VERSION, "feature_names": list(FEATURE_NAMES)}
