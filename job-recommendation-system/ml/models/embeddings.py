"""CPU embeddings with local-only loading, batching and a content-addressed cache."""

import hashlib
import json
import sqlite3
import threading
from collections import OrderedDict
from pathlib import Path
import numpy as np
from ml.preprocessing.text import clean_text


class EmbeddingService:
    def __init__(self, config, instance_path, encoder=None):
        self.enabled = bool(config.get("EMBEDDINGS_ENABLED", False))
        self.model_path = config.get("EMBEDDING_MODEL_PATH", "")
        self.model_name = config.get(
            "EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2"
        )
        self.revision = config.get("EMBEDDING_MODEL_REVISION", "unprepared")
        self.version = f"{self.model_name}@{self.revision}:text-v1"
        self.batch_size = int(config.get("EMBEDDING_BATCH_SIZE", 32))
        self.dimension = int(config.get("EMBEDDING_DIMENSION", 384))
        self.cache_path = Path(instance_path) / "ml" / "embeddings.sqlite"
        self.encoder = encoder
        self.attempted = encoder is not None
        self.lock = threading.RLock()
        self.memory = OrderedDict()
        self.reason = (
            "ready"
            if encoder is not None
            else "disabled" if not self.enabled else "not_loaded"
        )
        self.encoded = 0
        self.cache_hits = 0

    def load(self):
        with self.lock:
            if self.encoder is not None:
                return self.encoder
            if self.attempted or not self.enabled:
                return None
            self.attempted = True
            try:
                path = Path(self.model_path).resolve()
                if not self.model_path or not path.is_dir():
                    self.reason = "local_model_missing"
                    return None
                manifest = json.loads((path / "jobmatch-model.json").read_text())
                if (
                    manifest.get("model_name") != self.model_name
                    or manifest.get("revision") != self.revision
                ):
                    self.reason = "model_version_mismatch"
                    return None
                # Never execute remote Python code, or fetch weights from a request.
                from sentence_transformers import SentenceTransformer

                self.encoder = SentenceTransformer(
                    str(path),
                    device="cpu",
                    local_files_only=True,
                    trust_remote_code=False,
                    model_kwargs={"use_safetensors": True},
                )
                if self.encoder.get_sentence_embedding_dimension() != self.dimension:
                    self.encoder = None
                    self.reason = "dimension_mismatch"
                else:
                    self.reason = "ready"
            except Exception:
                self.reason = "unavailable_local_backend"
                self.encoder = None
            return self.encoder

    def key(self, text):
        return hashlib.sha256((self.version + "\0" + text).encode()).hexdigest()

    def _validate(self, vector):
        value = np.asarray(vector, dtype=np.float32)
        if value.shape != (self.dimension,) or not np.isfinite(value).all():
            raise ValueError("Invalid embedding vector.")
        norm = np.linalg.norm(value)
        return value / norm if norm > 0 else value

    def vectors(self, texts, persist=False):
        if not texts:
            return np.empty((0, self.dimension), dtype=np.float32)
        with self.lock:
            backend = self.load()
            if backend is None:
                return None
            try:
                prepared = [clean_text(text, 20000) for text in texts]
                keys = [self.key(text) for text in prepared]
                connection = None
                if persist:
                    self.cache_path.parent.mkdir(
                        parents=True, exist_ok=True, mode=0o700
                    )
                    connection = sqlite3.connect(self.cache_path, timeout=5)
                    self.cache_path.chmod(0o600)
                    connection.execute(
                        "CREATE TABLE IF NOT EXISTS embeddings (key TEXT PRIMARY KEY, model_version TEXT NOT NULL, dimension INTEGER NOT NULL, vector TEXT NOT NULL)"
                    )
                found, missing = {}, {}
                try:
                    for key, text in zip(keys, prepared):
                        if key in found:
                            continue
                        if key in self.memory:
                            found[key] = self.memory[key]
                            self.memory.move_to_end(key)
                            self.cache_hits += 1
                            continue
                        row = (
                            connection.execute(
                                "SELECT model_version, dimension, vector FROM embeddings WHERE key = ?",
                                (key,),
                            ).fetchone()
                            if connection
                            else None
                        )
                        if row and row[0] == self.version and row[1] == self.dimension:
                            try:
                                found[key] = self._validate(json.loads(row[2]))
                                self.cache_hits += 1
                                continue
                            except (ValueError, TypeError):
                                pass
                        missing[key] = text
                    if missing:
                        encoded = backend.encode(
                            list(missing.values()),
                            batch_size=self.batch_size,
                            normalize_embeddings=True,
                            convert_to_numpy=True,
                            show_progress_bar=False,
                        )
                        if len(encoded) != len(missing):
                            raise ValueError("Embedding batch length mismatch.")
                        for key, vector in zip(missing, encoded):
                            found[key] = self._validate(vector)
                            if connection:
                                connection.execute(
                                    "INSERT OR REPLACE INTO embeddings VALUES (?, ?, ?, ?)",
                                    (
                                        key,
                                        self.version,
                                        self.dimension,
                                        json.dumps(found[key].tolist()),
                                    ),
                                )
                        self.encoded += len(missing)
                    if connection:
                        connection.commit()
                    for key, vector in found.items():
                        self.memory[key] = vector
                        self.memory.move_to_end(key)
                    while len(self.memory) > 4096:
                        self.memory.popitem(last=False)
                    return np.stack([found[key] for key in keys])
                finally:
                    if connection:
                        connection.close()
            except Exception:
                self.reason = "embedding_or_cache_error"
                return None

    def similarities(self, candidate, jobs):
        job_vectors = self.vectors(jobs, persist=True)
        candidate_vectors = self.vectors([candidate], persist=False)
        if job_vectors is None or candidate_vectors is None:
            return None
        return np.clip(job_vectors @ candidate_vectors[0], 0, 1) * 100

    def status(self):
        return {
            "enabled": self.enabled,
            "available": self.encoder is not None,
            "status": self.reason,
            "model": self.model_name,
            "revision": self.revision,
            "dimension": self.dimension,
            "encoded": self.encoded,
            "cache_hits": self.cache_hits,
        }
