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
    is_active = db.Column(
        db.Boolean, nullable=False, default=True, server_default=db.true()
    )
    session_version = db.Column(
        db.Integer, nullable=False, default=1, server_default="1"
    )
    last_login_at = db.Column(db.DateTime)
    email_verified_at = db.Column(db.DateTime)
    remote_preference = db.Column(
        db.String(20), nullable=False, default="any", server_default="any"
    )
    salary_currency = db.Column(
        db.String(3), nullable=False, default="INR", server_default="INR"
    )
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
        from flask import current_app, has_app_context

        method = "scrypt"
        if has_app_context() and current_app.testing:
            method = current_app.config.get("TEST_PASSWORD_HASH_METHOD") or method
        self.password_hash = generate_password_hash(password, method=method)

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
    source = db.Column(
        db.String(40), nullable=False, default="demo", server_default="demo", index=True
    )
    source_name = db.Column(
        db.String(100), nullable=False, default="Demo", server_default="Demo"
    )
    external_id = db.Column(db.String(180))
    source_url = db.Column(db.Text, nullable=False, default="", server_default="")
    external_created_at = db.Column(db.DateTime)
    external_updated_at = db.Column(db.DateTime)
    last_synced_at = db.Column(db.DateTime, index=True)
    first_seen_at = db.Column(db.DateTime, default=utcnow, index=True)
    is_external = db.Column(
        db.Boolean, nullable=False, default=False, server_default=db.false(), index=True
    )
    raw_source_data = db.Column(
        db.JSON, nullable=False, default=dict, server_default="{}"
    )
    fingerprint = db.Column(db.String(64), unique=True)
    remote_type = db.Column(
        db.String(20), nullable=False, default="unknown", server_default="unknown"
    )
    remote_allowed = db.Column(
        db.Boolean, nullable=False, default=False, server_default=db.false()
    )
    salary_currency = db.Column(
        db.String(3), nullable=False, default="INR", server_default="INR"
    )
    salary_period = db.Column(
        db.String(20), nullable=False, default="year", server_default="year"
    )
    experience_known = db.Column(
        db.Boolean, nullable=False, default=True, server_default=db.true()
    )
    published = db.Column(
        db.Boolean, nullable=False, default=True, server_default=db.true()
    )
    archived = db.Column(
        db.Boolean, nullable=False, default=False, server_default=db.false()
    )
    deleted = db.Column(
        db.Boolean, nullable=False, default=False, server_default=db.false()
    )
    featured = db.Column(
        db.Boolean, nullable=False, default=False, server_default=db.false()
    )
    verified = db.Column(
        db.Boolean, nullable=False, default=False, server_default=db.false()
    )
    freshness_override = db.Column(
        db.String(30), nullable=False, default="auto", server_default="auto"
    )
    views = db.Column(db.Integer, default=0, nullable=False)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)
    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_jobs_source_external"),
        CheckConstraint("min_salary IS NULL OR min_salary >= 0"),
        CheckConstraint("max_salary IS NULL OR max_salary >= 0"),
        CheckConstraint(
            "min_salary IS NULL OR max_salary IS NULL OR max_salary >= min_salary"
        ),
        CheckConstraint("experience_min >= 0"),
        CheckConstraint("experience_max IS NULL OR experience_max >= experience_min"),
    )

    @property
    def freshness(self):
        from services.job_catalog import freshness_label

        return freshness_label(self)

    @property
    def salary_display(self):
        from services.job_catalog import salary_display

        return salary_display(self)

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
            "source",
            "source_name",
            "external_id",
            "source_url",
            "is_external",
            "remote_type",
            "remote_allowed",
            "salary_currency",
            "salary_period",
            "experience_known",
            "featured",
            "verified",
        ]
        result = {key: getattr(self, key) for key in keys}
        result["posted_date"] = self.posted_date.isoformat()
        result["application_deadline"] = (
            self.application_deadline.isoformat() if self.application_deadline else None
        )
        for key in ("external_created_at", "external_updated_at", "last_synced_at"):
            value = getattr(self, key)
            result[key] = value.isoformat() + "Z" if value else None
        result["freshness"] = self.freshness
        result["salary_display"] = self.salary_display
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
    notes = db.Column(db.Text, nullable=False, default="", server_default="")
    application_date = db.Column(db.Date)
    follow_up_date = db.Column(db.Date, index=True)
    company_contact = db.Column(
        db.String(254), nullable=False, default="", server_default=""
    )
    application_url = db.Column(db.Text, nullable=False, default="", server_default="")
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
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    source = db.Column(
        db.String(40), nullable=False, default="all", server_default="all"
    )
    location = db.Column(db.String(160), nullable=False, default="", server_default="")
    result_count = db.Column(db.Integer, nullable=False, default=0, server_default="0")
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False, index=True)


class SchemaRevision(db.Model):
    __tablename__ = "schema_revisions"
    version = db.Column(db.Integer, primary_key=True)
    applied_at = db.Column(db.DateTime, default=utcnow, nullable=False)


class PasswordResetToken(db.Model):
    __tablename__ = "password_reset_tokens"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token_hash = db.Column(db.String(64), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False, index=True)
    used_at = db.Column(db.DateTime)


class EmailVerificationToken(db.Model):
    __tablename__ = "email_verification_tokens"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    email = db.Column(db.String(254), nullable=False)
    token_hash = db.Column(db.String(64), nullable=False, unique=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime)


class UserSession(db.Model):
    __tablename__ = "user_sessions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token_hash = db.Column(db.String(64), nullable=False, unique=True)
    version = db.Column(db.Integer, nullable=False)
    remember = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    last_seen_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    expires_at = db.Column(db.DateTime, nullable=False, index=True)
    revoked_at = db.Column(db.DateTime)
    browser = db.Column(db.String(120), nullable=False, default="Browser")


class RateLimitBucket(db.Model):
    __tablename__ = "rate_limit_buckets"
    key = db.Column(db.String(64), primary_key=True)
    window_started = db.Column(db.DateTime, nullable=False, index=True)
    attempts = db.Column(db.Integer, nullable=False, default=0)


class ExternalJobIdentity(db.Model):
    __tablename__ = "external_job_identities"
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(40), nullable=False)
    external_id = db.Column(db.String(180), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False, index=True)
    source_url = db.Column(db.Text, nullable=False)
    last_seen_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    __table_args__ = (UniqueConstraint("provider", "external_id"),)


class ExternalJobCache(db.Model):
    __tablename__ = "external_job_cache"
    key = db.Column(db.String(64), primary_key=True)
    provider = db.Column(db.String(40), nullable=False, index=True)
    parameters = db.Column(db.JSON, nullable=False, default=dict)
    job_ids = db.Column(db.JSON, nullable=False, default=list)
    total = db.Column(db.Integer, nullable=False, default=0)
    fetched_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime, index=True)
    retry_after = db.Column(db.DateTime)
    lock_until = db.Column(db.DateTime)
    lock_token = db.Column(db.String(36))
    last_error = db.Column(db.String(160), default="")


class JobProvider(db.Model):
    __tablename__ = "job_providers"
    slug = db.Column(db.String(40), primary_key=True)
    enabled = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(db.String(30), nullable=False, default="not_checked")
    last_attempt = db.Column(db.DateTime)
    last_success = db.Column(db.DateTime)
    last_error = db.Column(db.String(160), nullable=False, default="")
    response_ms = db.Column(db.Integer)
    requests = db.Column(db.Integer, nullable=False, default=0)
    failures = db.Column(db.Integer, nullable=False, default=0)
    jobs_fetched = db.Column(db.Integer, nullable=False, default=0)
    jobs_inserted = db.Column(db.Integer, nullable=False, default=0)
    jobs_updated = db.Column(db.Integer, nullable=False, default=0)
    jobs_skipped = db.Column(db.Integer, nullable=False, default=0)


class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    kind = db.Column(db.String(40), nullable=False)
    title = db.Column(db.String(160), nullable=False)
    message = db.Column(db.String(600), nullable=False)
    link = db.Column(db.String(250), nullable=False, default="/dashboard")
    dedupe_key = db.Column(db.String(180), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow, index=True)
    read_at = db.Column(db.DateTime)
    __table_args__ = (UniqueConstraint("user_id", "dedupe_key"),)


class JobAlert(db.Model):
    __tablename__ = "job_alerts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name = db.Column(db.String(100), nullable=False)
    filters = db.Column(db.JSON, nullable=False, default=dict)
    frequency = db.Column(db.String(10), nullable=False, default="daily")
    email_enabled = db.Column(db.Boolean, nullable=False, default=False)
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    last_run_at = db.Column(db.DateTime)
    next_run_at = db.Column(db.DateTime, nullable=False, default=utcnow, index=True)
    lock_until = db.Column(db.DateTime)
    lock_token = db.Column(db.String(36))
    last_error = db.Column(db.String(160), nullable=False, default="")


class JobAlertDelivery(db.Model):
    __tablename__ = "job_alert_deliveries"
    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(
        db.Integer,
        db.ForeignKey("job_alerts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    email_sent = db.Column(db.Boolean, nullable=False, default=False)
    __table_args__ = (UniqueConstraint("alert_id", "job_id"),)


class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    action = db.Column(db.String(80), nullable=False, index=True)
    subject_type = db.Column(db.String(40), nullable=False, default="")
    subject_id = db.Column(db.String(80), nullable=False, default="")
    details = db.Column(db.JSON, nullable=False, default=dict)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow, index=True)


class SiteSetting(db.Model):
    __tablename__ = "site_settings"
    key = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.JSON, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=utcnow, onupdate=utcnow)


class JobView(db.Model):
    __tablename__ = "job_views"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    viewed_at = db.Column(db.DateTime, nullable=False, default=utcnow, index=True)
    job = db.relationship("Job")
    __table_args__ = (UniqueConstraint("user_id", "job_id"),)
