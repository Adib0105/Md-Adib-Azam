"""Relational storage. Personal records are always scoped to their owner."""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, CheckConstraint, UniqueConstraint
from sqlalchemy.engine import Engine
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

db = SQLAlchemy()


def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


@event.listens_for(Engine, "connect")
def sqlite_foreign_keys(connection, _):
    if isinstance(connection, sqlite3.Connection):
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA busy_timeout=5000")


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    phone = db.Column(db.String(30), default="")
    city = db.Column(db.String(80), default="")
    state = db.Column(db.String(80), default="")
    country = db.Column(db.String(80), default="India")
    education = db.Column(db.String(180), default="")
    experience_years = db.Column(db.Float, nullable=True)
    experience_summary = db.Column(db.Text, default="")
    preferred_role = db.Column(db.String(160), default="")
    preferred_location = db.Column(db.String(160), default="")
    expected_salary = db.Column(db.Integer, nullable=True)
    employment_type = db.Column(db.String(50), default="")
    willing_to_relocate = db.Column(db.Boolean, default=False)
    certifications = db.Column(db.Text, default="")
    projects = db.Column(db.Text, default="")
    career_interests = db.Column(db.Text, default="")
    resume_text = db.Column(db.Text, default="")
    resume_filename = db.Column(db.String(200), default="")
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)
    skills = db.relationship(
        "CandidateSkill", backref="user", cascade="all, delete-orphan", lazy="selectin"
    )
    __table_args__ = (
        CheckConstraint("experience_years IS NULL OR experience_years >= 0"),
        CheckConstraint("expected_salary IS NULL OR expected_salary >= 0"),
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def skill_names(self):
        return [s.skill_name for s in self.skills]


class CandidateSkill(db.Model):
    __tablename__ = "candidate_skills"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    skill_name = db.Column(db.String(100), nullable=False)
    proficiency_level = db.Column(db.String(20), default="Intermediate", nullable=False)
    __table_args__ = (UniqueConstraint("user_id", "skill_name"),)


class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.String(80), unique=True)
    job_title = db.Column(db.String(160), nullable=False, index=True)
    company_name = db.Column(db.String(160), nullable=False, index=True)
    job_description = db.Column(db.Text, nullable=False, default="")
    required_skills = db.Column(db.JSON, nullable=False, default=list)
    preferred_skills = db.Column(db.JSON, nullable=False, default=list)
    location = db.Column(
        db.String(100), nullable=False, default="Unspecified", index=True
    )
    state = db.Column(db.String(80), default="")
    min_salary = db.Column(db.Integer, nullable=True)
    max_salary = db.Column(db.Integer, nullable=True)
    experience_min = db.Column(db.Float, nullable=False, default=0)
    experience_max = db.Column(db.Float, nullable=True)
    employment_type = db.Column(db.String(50), nullable=False, default="Full-time")
    industry = db.Column(db.String(80), nullable=False, default="Other")
    education_required = db.Column(db.String(160), default="")
    posted_date = db.Column(db.Date, nullable=False)
    application_deadline = db.Column(db.Date, nullable=True)
    company_rating = db.Column(db.Float, nullable=True)
    active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    is_synthetic = db.Column(db.Boolean, default=True, nullable=False)
    views = db.Column(db.Integer, default=0, nullable=False)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)
    __table_args__ = (
        CheckConstraint("min_salary IS NULL OR min_salary >= 0"),
        CheckConstraint("max_salary IS NULL OR max_salary >= 0"),
        CheckConstraint(
            "min_salary IS NULL OR max_salary IS NULL OR max_salary >= min_salary"
        ),
        CheckConstraint("experience_min >= 0"),
        CheckConstraint("experience_max IS NULL OR experience_max >= experience_min"),
    )

    def as_dict(self):
        keys = [
            "id",
            "job_title",
            "company_name",
            "job_description",
            "required_skills",
            "preferred_skills",
            "location",
            "state",
            "min_salary",
            "max_salary",
            "experience_min",
            "experience_max",
            "employment_type",
            "industry",
            "education_required",
            "company_rating",
            "is_synthetic",
            "active",
        ]
        result = {key: getattr(self, key) for key in keys}
        result["posted_date"] = self.posted_date.isoformat()
        result["application_deadline"] = (
            self.application_deadline.isoformat() if self.application_deadline else None
        )
        return result


class SavedJob(db.Model):
    __tablename__ = "saved_jobs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    job = db.relationship("Job")
    __table_args__ = (UniqueConstraint("user_id", "job_id"),)


class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    status = db.Column(db.String(30), default="Applied", nullable=False)
    applied_date = db.Column(db.DateTime, default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)
    job = db.relationship("Job")
    __table_args__ = (UniqueConstraint("user_id", "job_id"),)


class RecommendationRun(db.Model):
    __tablename__ = "recommendation_runs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    fingerprint = db.Column(db.String(64), nullable=False)
    reason = db.Column(db.String(60), default="profile")
    profile_summary = db.Column(db.JSON, nullable=False, default=dict)
    weights = db.Column(db.JSON, nullable=False, default=dict)
    results = db.relationship(
        "Recommendation", backref="run", cascade="all, delete-orphan", lazy="selectin"
    )


class Recommendation(db.Model):
    __tablename__ = "recommendations"
    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(
        db.Integer,
        db.ForeignKey("recommendation_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False, index=True)
    job_title = db.Column(db.String(160), nullable=False)
    company_name = db.Column(db.String(160), nullable=False)
    overall_score = db.Column(db.Float, nullable=False)
    scores = db.Column(db.JSON, nullable=False)
    __table_args__ = (UniqueConstraint("run_id", "job_id"),)


class ResumeDraft(db.Model):
    __tablename__ = "resume_drafts"
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    filename = db.Column(db.String(200), nullable=False)
    extracted = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)


class SearchEvent(db.Model):
    __tablename__ = "search_events"
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(160), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False, index=True)
