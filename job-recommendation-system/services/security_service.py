"""Shared rate limits, revocable sessions and metadata-only audit events."""

import hashlib
import hmac
import secrets
from datetime import timedelta
from flask import current_app, request, session, g, has_request_context, abort
from sqlalchemy.exc import IntegrityError
from models.database import db, User, UserSession, RateLimitBucket, AuditLog, utcnow


def token_hash(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def audit(action, *, actor_id=None, subject_type="", subject_id="", details=None):
    if actor_id is None and has_request_context() and g.get("user"):
        actor_id = g.user.id
    # Callers supply identifiers/counts only, never credentials or request bodies.
    db.session.add(
        AuditLog(
            actor_id=actor_id,
            action=action[:80],
            subject_type=subject_type[:40],
            subject_id=str(subject_id)[:80],
            details=details or {},
        )
    )
    current_app.logger.info(action, extra={"event": action, "actor_id": actor_id})


def consume_limit(scope, identity, maximum, seconds):
    key = hmac.new(
        str(current_app.config["SECRET_KEY"]).encode(),
        f"{scope}|{identity}".encode(),
        hashlib.sha256,
    ).hexdigest()
    now = utcnow()
    bucket = db.session.get(RateLimitBucket, key)
    if not bucket:
        try:
            db.session.add(RateLimitBucket(key=key, window_started=now, attempts=0))
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
    db.session.execute(
        db.update(RateLimitBucket)
        .where(
            RateLimitBucket.key == key,
            RateLimitBucket.window_started <= now - timedelta(seconds=seconds),
        )
        .values(window_started=now, attempts=0)
    )
    changed = db.session.execute(
        db.update(RateLimitBucket)
        .where(RateLimitBucket.key == key, RateLimitBucket.attempts < maximum)
        .values(attempts=RateLimitBucket.attempts + 1)
    ).rowcount
    db.session.commit()
    return bool(changed)


def rate_limit(scope, maximum, seconds, subject=""):
    identity = f"{request.remote_addr or 'unknown'}|{subject}"
    if not consume_limit(scope, identity, maximum, seconds):
        abort(429, description="Too many requests. Please wait before trying again.")


def start_session(user, remember=False):
    session.clear()
    raw = secrets.token_urlsafe(32)
    now = utcnow()
    duration = (
        timedelta(days=current_app.config["REMEMBER_DAYS"])
        if remember
        else timedelta(hours=current_app.config["SESSION_HOURS"])
    )
    record = UserSession(
        user_id=user.id,
        token_hash=token_hash(raw),
        version=user.session_version,
        remember=remember,
        expires_at=now + duration,
        browser=(request.user_agent.browser or "Browser")[:120],
    )
    db.session.add(record)
    user.last_login_at = now
    db.session.commit()
    session["user_id"] = user.id
    session["auth_token"] = raw
    session.permanent = remember
    return record


def load_session_user():
    g.user = None
    g.auth_session = None
    raw = session.get("auth_token", "")
    user_id = session.get("user_id")
    if not isinstance(raw, str) or not raw or not user_id:
        if user_id:
            session.clear()
        return
    record = db.session.scalar(
        db.select(UserSession).where(
            UserSession.token_hash == token_hash(raw), UserSession.user_id == user_id
        )
    )
    user = db.session.get(User, user_id)
    now = utcnow()
    idle = (
        timedelta(days=current_app.config["REMEMBER_DAYS"])
        if record and record.remember
        else timedelta(minutes=current_app.config["SESSION_IDLE_MINUTES"])
    )
    if (
        not record
        or not user
        or not user.is_active
        or record.revoked_at
        or record.expires_at <= now
        or record.version != user.session_version
        or record.last_seen_at + idle <= now
    ):
        session.clear()
        return
    g.user, g.auth_session = user, record
    if record.last_seen_at < now - timedelta(minutes=5):
        record.last_seen_at = now
        db.session.commit()


def revoke_sessions(user):
    db.session.flush()
    db.session.execute(
        db.update(User)
        .where(User.id == user.id)
        .values(session_version=User.session_version + 1)
    )
    db.session.execute(
        db.update(UserSession)
        .where(UserSession.user_id == user.id, UserSession.revoked_at.is_(None))
        .values(revoked_at=utcnow())
    )
