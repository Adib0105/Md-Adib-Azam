"""Portable TF-IDF cache without pickle or executable model deserialization."""

import json
import zipfile
from uuid import uuid4
import numpy as np
import sklearn
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer


def save_cache(path, signature, features):
    arrays = {
        "metadata": np.array(
            json.dumps(
                {
                    "signature": signature,
                    "sklearn": sklearn.__version__,
                    "format": "tfidf-v2",
                }
            )
        )
    }
    for prefix, vectorizer, matrix in [
        ("text", features[0], features[1]),
        ("role", features[2], features[3]),
    ]:
        arrays.update(
            {
                prefix
                + "_vocabulary": np.array(
                    json.dumps(
                        {
                            key: int(value)
                            for key, value in vectorizer.vocabulary_.items()
                        }
                    )
                ),
                prefix + "_idf": vectorizer.idf_,
                prefix + "_data": matrix.data,
                prefix + "_indices": matrix.indices,
                prefix + "_indptr": matrix.indptr,
                prefix + "_shape": np.array(matrix.shape),
            }
        )
    temporary = path.with_name(f"tfidf-{uuid4().hex}.tmp")
    try:
        with temporary.open("wb") as handle:
            np.savez_compressed(handle, **arrays)
        temporary.chmod(0o600)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def load_cache(path, signature):
    if path.stat().st_size > 64 * 1024 * 1024:
        raise ValueError("TF-IDF cache exceeds the size bound.")
    with zipfile.ZipFile(path) as archive:
        if (
            len(archive.infolist()) > 20
            or sum(item.file_size for item in archive.infolist()) > 128 * 1024 * 1024
        ):
            raise ValueError("Expanded TF-IDF cache exceeds the size bound.")
    with np.load(path, allow_pickle=False) as arrays:
        metadata = json.loads(str(arrays["metadata"]))
        if metadata != {
            "signature": signature,
            "sklearn": sklearn.__version__,
            "format": "tfidf-v2",
        }:
            return None
        result = []
        for prefix in ["text", "role"]:
            vocabulary = json.loads(str(arrays[prefix + "_vocabulary"]))
            if not isinstance(vocabulary, dict) or len(vocabulary) > 50000:
                raise ValueError("Invalid vocabulary.")
            if sorted(vocabulary.values()) != list(range(len(vocabulary))):
                raise ValueError("Invalid vocabulary indices.")
            vectorizer = TfidfVectorizer(
                ngram_range=(1, 2),
                sublinear_tf=True,
                stop_words="english" if prefix == "text" else None,
                vocabulary=vocabulary,
            )
            idf = arrays[prefix + "_idf"]
            if (
                idf.shape != (len(vocabulary),)
                or not np.isfinite(idf).all()
                or (idf < 1).any()
            ):
                raise ValueError("Invalid IDF vector.")
            vectorizer.idf_ = idf
            matrix = csr_matrix(
                (
                    arrays[prefix + "_data"],
                    arrays[prefix + "_indices"],
                    arrays[prefix + "_indptr"],
                ),
                shape=tuple(arrays[prefix + "_shape"]),
            )
            matrix.check_format(full_check=True)
            if (
                matrix.shape[1] != len(vocabulary)
                or matrix.shape[0] > 10000
                or not np.isfinite(matrix.data).all()
            ):
                raise ValueError("Invalid TF-IDF matrix.")
            result.extend([vectorizer, matrix])
    return tuple(result)
