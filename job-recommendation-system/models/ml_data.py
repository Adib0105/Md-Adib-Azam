"""Additive tables; append-only feedback and recorded model assignments."""

from models.database import db, utcnow
from sqlalchemy import UniqueConstraint, CheckConstraint, Index


class InteractionEvent(db.Model):
    __tablename__ = "interaction_events"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False, index=True)
    action = db.Column(db.String(30), nullable=False)
    origin = db.Column(db.String(40), nullable=False, default="explicit")
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False, index=True)
    job = db.relationship("Job")
    __table_args__ = (
        CheckConstraint(
            "action IN ('viewed','saved','unsaved','applied','rejected','ignored','interview','offer','outcome_rejected')"
        ),
        Index("ix_interaction_user_time", "user_id", "created_at"),
    )


class Experiment(db.Model):
    __tablename__ = "ml_experiments"
    slug = db.Column(db.String(80), primary_key=True)
    version = db.Column(db.String(40), nullable=False, default="v1")
    model_a = db.Column(db.String(30), nullable=False, default="weighted")
    model_b = db.Column(db.String(30), nullable=False, default="hybrid")
    enabled = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    description = db.Column(db.String(600), nullable=False, default="")


class ExperimentAssignment(db.Model):
    __tablename__ = "ml_experiment_assignments"
    id = db.Column(db.Integer, primary_key=True)
    experiment_slug = db.Column(
        db.String(80), db.ForeignKey("ml_experiments.slug"), nullable=False, index=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    variant = db.Column(db.String(1), nullable=False)
    strategy = db.Column(db.String(30), nullable=False)
    model_version = db.Column(db.String(80), nullable=False)
    assigned_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    __table_args__ = (
        UniqueConstraint("experiment_slug", "user_id"),
        CheckConstraint("variant IN ('A','B')"),
    )


class RecommendationExposure(db.Model):
    __tablename__ = "recommendation_exposures"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False, index=True)
    assignment_id = db.Column(
        db.Integer, db.ForeignKey("ml_experiment_assignments.id"), index=True
    )
    request_id = db.Column(db.String(36), nullable=False, index=True)
    strategy = db.Column(db.String(30), nullable=False)
    model_version = db.Column(db.String(100), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False, index=True)
    __table_args__ = (
        UniqueConstraint("request_id", "job_id"),
        Index("ix_exposure_user_job_time", "user_id", "job_id", "created_at"),
    )
