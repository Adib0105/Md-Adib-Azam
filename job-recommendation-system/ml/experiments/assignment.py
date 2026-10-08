"""Experiments are disabled by default; assignment is saved before exposure."""

import hashlib
import hmac
from uuid import uuid4
from flask import current_app
from sqlalchemy.exc import IntegrityError
from models.database import db
from models.ml_data import Experiment, ExperimentAssignment, RecommendationExposure
from ml import PIPELINE_VERSION


def strategy_for(user):
    slug = current_app.config.get("ML_EXPERIMENT", "")
    experiment = db.session.get(Experiment, slug) if slug else None
    if not experiment or not experiment.enabled or user.is_admin:
        return current_app.config["ML_STRATEGY"], None
    if {experiment.model_a, experiment.model_b} != {"weighted", "hybrid"}:
        raise ValueError("This experiment supports weighted versus hybrid only.")
    assignment = db.session.scalar(
        db.select(ExperimentAssignment).where(
            ExperimentAssignment.user_id == user.id,
            ExperimentAssignment.experiment_slug == slug,
        )
    )
    if assignment is None:
        digest = hmac.new(
            str(current_app.config["SECRET_KEY"]).encode(),
            f"{slug}|{experiment.version}|{user.id}".encode(),
            hashlib.sha256,
        ).digest()
        variant = "A" if digest[0] < 128 else "B"
        strategy = experiment.model_a if variant == "A" else experiment.model_b
        try:
            with db.session.begin_nested():
                assignment = ExperimentAssignment(
                    experiment_slug=slug,
                    user_id=user.id,
                    variant=variant,
                    strategy=strategy,
                    model_version=(
                        "seven-factor-v2"
                        if strategy == "weighted"
                        else PIPELINE_VERSION
                    ),
                )
                db.session.add(assignment)
                db.session.flush()
            db.session.commit()
        except IntegrityError:
            assignment = db.session.scalar(
                db.select(ExperimentAssignment).where(
                    ExperimentAssignment.user_id == user.id,
                    ExperimentAssignment.experiment_slug == slug,
                )
            )
    return assignment.strategy, assignment


def record_exposure(user, rows):
    """Record only jobs actually returned on this page, with their displayed positions."""
    if user.is_admin or not rows:
        return
    _, assignment = strategy_for(user)
    request_id = str(uuid4())
    for position, row in enumerate(rows, 1):
        model = row.get("model", {"strategy": "weighted", "version": "seven-factor-v2"})
        db.session.add(
            RecommendationExposure(
                user_id=user.id,
                job_id=row["job"].id,
                request_id=request_id,
                assignment_id=assignment.id if assignment else None,
                strategy=model["strategy"],
                model_version=model["version"],
                position=position,
                score=row["score"],
            )
        )
    db.session.commit()
