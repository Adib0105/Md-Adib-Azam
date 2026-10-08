"""Freeze the training vocabularies/IDF so ranker inference uses the same features."""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

REPRESENTATION_VERSION = "identity-minimized-tfidf-v2"


def serialize_representation(features, embedding_version=None):
    return {
        "version": REPRESENTATION_VERSION,
        "embedding_version": embedding_version,
        "text": {
            "vocabulary": {
                key: int(index) for key, index in features[0].vocabulary_.items()
            },
            "idf": features[0].idf_.tolist(),
        },
        "role": {
            "vocabulary": {
                key: int(index) for key, index in features[2].vocabulary_.items()
            },
            "idf": features[2].idf_.tolist(),
        },
    }


def load_representation(value):
    if not isinstance(value, dict) or value.get("version") != REPRESENTATION_VERSION:
        raise ValueError("Incompatible text representation version.")
    result = []
    for kind in ["text", "role"]:
        vocabulary = value[kind]["vocabulary"]
        if (
            not isinstance(vocabulary, dict)
            or not 1 <= len(vocabulary) <= 20000
            or sorted(vocabulary.values()) != list(range(len(vocabulary)))
            or any(not isinstance(key, str) for key in vocabulary)
        ):
            raise ValueError("Invalid frozen vocabulary.")
        idf = np.asarray(value[kind]["idf"], dtype=float)
        if (
            idf.shape != (len(vocabulary),)
            or not np.isfinite(idf).all()
            or (idf < 1).any()
        ):
            raise ValueError("Invalid frozen IDF.")
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            stop_words="english" if kind == "text" else None,
            vocabulary=vocabulary,
        )
        vectorizer.idf_ = idf
        result.extend([vectorizer, None])
    return tuple(result)
