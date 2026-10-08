"""Experimental pointwise learning-to-rank with safe, portable JSON inference.

Expected ordinal relevance is a ranking utility, never a hiring probability.
"""

import hashlib
import importlib.metadata
import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from ml.features.schema import FEATURE_NAMES, contract, validate_matrix
from ml.features.representation import load_representation

ARTIFACT_VERSION = "jobmatch-ranker-v1"
MAX_ARTIFACT_BYTES = 8 * 1024 * 1024


def canonical(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode()


def dependency_versions():
    return {
        name: importlib.metadata.version(name)
        for name in ["numpy", "scipy", "scikit-learn"]
    }


def train_ranker(
    matrix,
    labels,
    model_type="logistic",
    *,
    dataset_version,
    dataset_kind,
    metrics=None,
    representation=None,
):
    matrix = validate_matrix(matrix)
    labels = np.asarray(labels)
    if labels.shape != (len(matrix),) or len(matrix) < 8:
        raise ValueError("At least eight aligned training judgments are required.")
    if not np.isin(labels, [0, 1, 2, 3]).all() or len(set(labels.tolist())) < 2:
        raise ValueError(
            "Relevance labels must include at least two ordinal classes (0–3)."
        )
    if model_type == "logistic":
        estimator = LogisticRegression(
            max_iter=1500, random_state=2026, class_weight="balanced", C=1.0
        )
        estimator.fit(matrix, labels)
        model = {
            "classes": estimator.classes_.tolist(),
            "coefficients": estimator.coef_.tolist(),
            "intercepts": estimator.intercept_.tolist(),
        }
        importance = np.mean(np.abs(estimator.coef_), axis=0)
    elif model_type == "random_forest":
        estimator = RandomForestRegressor(
            n_estimators=48,
            max_depth=6,
            min_samples_leaf=2,
            random_state=2026,
            n_jobs=1,
        )
        estimator.fit(matrix, labels)
        model = {
            "trees": [
                {
                    "left": tree.tree_.children_left.tolist(),
                    "right": tree.tree_.children_right.tolist(),
                    "feature": tree.tree_.feature.tolist(),
                    "threshold": tree.tree_.threshold.tolist(),
                    "value": tree.tree_.value[:, 0, 0].tolist(),
                }
                for tree in estimator.estimators_
            ]
        }
        importance = estimator.feature_importances_
    else:
        raise ValueError("Choose logistic or random_forest.")
    if representation is not None:
        load_representation(representation)
        model["representation"] = representation
    metadata = {
        **contract(),
        "artifact_version": ARTIFACT_VERSION,
        "model_name": f"jobmatch-{model_type}",
        "model_type": model_type,
        "version": "1.0.0",
        "training_date": datetime.now(timezone.utc).isoformat(),
        "dataset_version": dataset_version,
        "dataset_kind": dataset_kind,
        "training_samples": len(labels),
        "dependency_versions": dependency_versions(),
        "metrics": metrics or {},
        "parameters": estimator.get_params(),
        "feature_importance": {
            name: round(float(value), 8)
            for name, value in zip(FEATURE_NAMES, importance)
        },
        "importance_method": (
            "mean absolute logistic coefficients"
            if model_type == "logistic"
            else "training impurity importance (can be biased)"
        ),
        "output": "expected ordinal relevance / 3; uncalibrated ranking utility",
    }
    artifact = {"metadata": metadata, "model": model}
    artifact["sha256"] = hashlib.sha256(canonical(artifact)).hexdigest()
    predictor = PortableRanker(artifact)
    expected = (
        estimator.predict_proba(matrix) @ estimator.classes_ / 3 * 100
        if model_type == "logistic"
        else estimator.predict(matrix) / 3 * 100
    )
    if not np.allclose(predictor.predict(matrix), expected, atol=1e-6):
        raise ValueError("Portable inference failed parity with its fitted estimator.")
    return predictor


class PortableRanker:
    def __init__(self, artifact):
        if not isinstance(artifact, dict) or set(artifact) != {
            "metadata",
            "model",
            "sha256",
        }:
            raise ValueError("Invalid model envelope.")
        body = {key: artifact[key] for key in ["metadata", "model"]}
        if hashlib.sha256(canonical(body)).hexdigest() != artifact["sha256"]:
            raise ValueError("Model integrity digest mismatch.")
        self.metadata = artifact["metadata"]
        required = {
            "model_name",
            "model_type",
            "version",
            "training_date",
            "dataset_version",
            "dataset_kind",
            "dependency_versions",
            "metrics",
            "parameters",
        }
        if not isinstance(self.metadata, dict) or not required <= set(self.metadata):
            raise ValueError("Missing model metadata.")
        if self.metadata.get("artifact_version") != ARTIFACT_VERSION or any(
            self.metadata.get(key) != value for key, value in contract().items()
        ):
            raise ValueError("Incompatible model/feature version.")
        if self.metadata["dependency_versions"] != dependency_versions():
            raise ValueError("Incompatible model dependency versions; retrain locally.")
        if self.metadata["dataset_kind"] not in {"synthetic", "manual", "behavioral"}:
            raise ValueError("Invalid model dataset provenance.")
        self.kind = self.metadata["model_type"]
        self.model = artifact["model"]
        self.artifact = artifact
        self.representation = self.model.get("representation")
        if self.representation is not None:
            load_representation(self.representation)
        if self.kind == "logistic":
            self.classes = np.asarray(self.model["classes"], dtype=float)
            self.coefficients = np.asarray(self.model["coefficients"], dtype=float)
            self.intercepts = np.asarray(self.model["intercepts"], dtype=float)
            if (
                len(self.classes) < 2
                or len(set(self.classes)) != len(self.classes)
                or not np.isin(self.classes, [0, 1, 2, 3]).all()
            ):
                raise ValueError("Invalid ordinal classes.")
            expected_rows = 1 if len(self.classes) == 2 else len(self.classes)
            if self.coefficients.shape != (
                expected_rows,
                len(FEATURE_NAMES),
            ) or self.intercepts.shape != (expected_rows,):
                raise ValueError("Invalid logistic coefficient shape.")
            if (
                not np.isfinite(self.coefficients).all()
                or not np.isfinite(self.intercepts).all()
            ):
                raise ValueError("Non-finite model coefficients.")
        elif self.kind == "random_forest":
            trees = self.model.get("trees", [])
            if not 1 <= len(trees) <= 128:
                raise ValueError("Invalid number of trees.")
            for tree in trees:
                length = len(tree.get("feature", []))
                if not 1 <= length <= 4096 or any(
                    len(tree.get(key, [])) != length
                    for key in ["left", "right", "threshold", "value"]
                ):
                    raise ValueError("Invalid tree arrays.")
                if (
                    not np.isfinite(tree["threshold"]).all()
                    or not np.isfinite(tree["value"]).all()
                ):
                    raise ValueError("Non-finite tree data.")
                visited = set()

                def visit(node, depth):
                    if (
                        not isinstance(node, int)
                        or not 0 <= node < length
                        or node in visited
                        or depth > 32
                    ):
                        raise ValueError("Invalid or cyclic tree.")
                    visited.add(node)
                    if tree["left"][node] == tree["right"][node] == -1:
                        return
                    feature = tree["feature"][node]
                    if not isinstance(feature, int) or not 0 <= feature < len(
                        FEATURE_NAMES
                    ):
                        raise ValueError("Invalid tree feature.")
                    visit(tree["left"][node], depth + 1)
                    visit(tree["right"][node], depth + 1)

                visit(0, 0)
                if len(visited) != length:
                    raise ValueError("Unreachable model nodes.")
        else:
            raise ValueError("Unsupported model type.")

    def predict(self, matrix):
        matrix = validate_matrix(matrix)
        if not len(matrix):
            return np.empty(0)
        if self.kind == "logistic":
            logits = matrix @ self.coefficients.T + self.intercepts
            if len(self.classes) == 2:
                positive = 1 / (1 + np.exp(-np.clip(logits[:, 0], -700, 700)))
                values = (1 - positive) * self.classes[0] + positive * self.classes[1]
            else:
                logits -= logits.max(axis=1, keepdims=True)
                probabilities = np.exp(logits)
                probabilities /= probabilities.sum(axis=1, keepdims=True)
                values = probabilities @ self.classes
        else:
            estimates = []
            for tree in self.model["trees"]:
                nodes = np.zeros(len(matrix), dtype=int)
                while True:
                    advancing = [
                        i for i, node in enumerate(nodes) if tree["left"][node] != -1
                    ]
                    if not advancing:
                        break
                    for i in advancing:
                        node = nodes[i]
                        nodes[i] = (
                            tree["left"][node]
                            if matrix[i, tree["feature"][node]]
                            <= tree["threshold"][node]
                            else tree["right"][node]
                        )
                estimates.append([tree["value"][node] for node in nodes])
            values = np.mean(estimates, axis=0)
        return np.clip(values / 3 * 100, 0, 100)

    def frozen_features(self):
        return (
            load_representation(self.representation)
            if self.representation is not None
            else None
        )

    def set_metrics(self, metrics):
        self.metadata["metrics"] = metrics
        self.artifact["sha256"] = hashlib.sha256(
            canonical({"metadata": self.metadata, "model": self.model})
        ).hexdigest()

    def explain(self, matrix):
        matrix = validate_matrix(matrix)
        original = self.predict(matrix)
        effects = {}
        for index, name in enumerate(FEATURE_NAMES):
            ablated = matrix.copy()
            ablated[:, index] = 0
            effects[name] = (original - self.predict(ablated)).tolist()
        return effects

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        temporary = path.with_name(f"ranker-{uuid4().hex}.tmp")
        try:
            temporary.write_bytes(canonical(self.artifact))
            temporary.chmod(0o600)
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)

    @classmethod
    def load(cls, path):
        path = Path(path)
        if path.is_symlink() or path.stat().st_size > MAX_ARTIFACT_BYTES:
            raise ValueError("Model artifact is a symlink or exceeds the size limit.")
        return cls(json.loads(path.read_text(encoding="utf-8")))


class RankerRegistry:
    """One local operator-owned artifact; bad artifacts cannot break recommendations."""

    def __init__(self, instance_path, allow_synthetic=False):
        self.path = Path(instance_path) / "ml" / "ranker.json"
        self.allow_synthetic = allow_synthetic
        self.signature = None
        self.ranker = None
        self.reason = "not_trained"
        self.lock = threading.RLock()

    def load(self):
        with self.lock:
            return self._load()

    def _load(self):
        try:
            info = self.path.stat()
            signature = (info.st_mtime_ns, info.st_size)
            if signature == self.signature:
                return self.ranker
            self.signature = signature
            self.ranker = PortableRanker.load(self.path)
            if self.ranker.representation is None:
                self.ranker = None
                self.reason = "feature_pipeline_missing"
            elif (
                self.ranker.metadata["dataset_kind"] == "synthetic"
                and not self.allow_synthetic
            ):
                self.ranker = None
                self.reason = "synthetic_model_not_enabled"
            else:
                self.reason = "ready"
        except FileNotFoundError:
            self.ranker = None
            self.signature = None
            self.reason = "not_trained"
        except (ValueError, TypeError, KeyError, OSError, OverflowError):
            self.ranker = None
            self.reason = "invalid_or_incompatible_artifact"
        return self.ranker
