"""Single-use, expiring recovery/verification tokens; only hashes enter the DB."""

import secrets
from datetime import timedelta
from flask import current_app
from sqlalchemy.exc import IntegrityError
from models.database import db, User, PasswordResetToken, EmailVerificationToken, utcnow
from services.security_service import audit, token_hash, revoke_sessions
from services.mail_service import queue_mail
from utils.validators import validate_password, validate_email, ValidationError

RESET_RESPONSE = (
    "If an active account uses that email, password-reset instructions will be sent."
)


def request_password_reset(email):
    try:
        email = validate_email(str(email))
    except ValidationError:
        return
    user = db.session.scalar(
        db.select(User).where(User.email == email, User.is_active.is_(True))
    )
    audit("password_reset_requested")
    if not user:
        db.session.commit()
        return
    raw = secrets.token_urlsafe(32)
    now = utcnow()
    db.session.execute(
        db.update(PasswordResetToken)
        .where(
            PasswordResetToken.user_id == user.id, PasswordResetToken.used_at.is_(None)
        )
        .values(used_at=now)
    )
    db.session.add(
        PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash(raw),
            expires_at=now
            + timedelta(minutes=current_app.config["RESET_TOKEN_MINUTES"]),
        )
    )
    db.session.commit()
    url = current_app.config["APP_BASE_URL"] + "/reset-password?token=" + raw
    queue_mail(
        user.email,
        "Reset your JobMatch password",
        f"A password reset was requested for your JobMatch account.\n\n{url}\n\nThis link expires in {current_app.config['RESET_TOKEN_MINUTES']} minutes and works once. If you did not request this, ignore this email.\n",
    )


def reset_password(raw, password, confirmation):
    if not isinstance(raw, str) or not 32 <= len(raw) <= 128:
        raise ValidationError("This reset link is invalid or expired.")
    validate_password(password)
    if password != confirmation:
        raise ValidationError("Your passwords do not match.")
    token = db.session.scalar(
        db.select(PasswordResetToken).where(
            PasswordResetToken.token_hash == token_hash(raw)
        )
    )
    now = utcnow()
    user = db.session.get(User, token.user_id) if token else None
    if (
        not token
        or token.used_at
        or token.expires_at <= now
        or not user
        or not user.is_active
    ):
        raise ValidationError("This reset link is invalid or expired.")
    temporary = User()
    temporary.set_password(password)
    changed = db.session.execute(
        db.update(PasswordResetToken)
        .where(
            PasswordResetToken.id == token.id,
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.expires_at > utcnow(),
        )
        .values(used_at=utcnow())
    ).rowcount
    if not changed:
        db.session.rollback()
        raise ValidationError("This reset link is invalid or expired.")
    user.password_hash = temporary.password_hash
    user.email_verified_at = utcnow()
    revoke_sessions(user)
    db.session.execute(
        db.update(EmailVerificationToken)
        .where(
            EmailVerificationToken.user_id == user.id,
            EmailVerificationToken.used_at.is_(None),
        )
        .values(used_at=utcnow())
    )
    db.session.execute(
        db.update(PasswordResetToken)
        .where(
            PasswordResetToken.user_id == user.id, PasswordResetToken.used_at.is_(None)
        )
        .values(used_at=utcnow())
    )
    audit("password_reset_completed", actor_id=user.id)
    db.session.commit()
    return user


def change_password(user, current, password, confirmation):
    if not user.check_password(current):
        raise ValidationError("Current password is incorrect.")
    validate_password(password)
    if password != confirmation:
        raise ValidationError("Your passwords do not match.")
    previous = user.password_hash
    temporary = User()
    temporary.set_password(password)
    updated = db.session.execute(
        db.update(User)
        .where(User.id == user.id, User.password_hash == previous)
        .values(password_hash=temporary.password_hash)
    ).rowcount
    if not updated:
        db.session.rollback()
        raise ValidationError("Account security changed. Sign in and try again.")
    revoke_sessions(user)
    db.session.execute(
        db.update(EmailVerificationToken)
        .where(
            EmailVerificationToken.user_id == user.id,
            EmailVerificationToken.used_at.is_(None),
        )
        .values(used_at=utcnow())
    )
    db.session.execute(
        db.update(PasswordResetToken)
        .where(
            PasswordResetToken.user_id == user.id, PasswordResetToken.used_at.is_(None)
        )
        .values(used_at=utcnow())
    )
    audit("password_changed", actor_id=user.id)
    db.session.commit()


def request_email_verification(user, email, password):
    if not user.check_password(password):
        raise ValidationError("Current password is incorrect.")
    email = validate_email(email)
    if db.session.scalar(
        db.select(User.id).where(User.email == email, User.id != user.id)
    ):
        raise ValidationError("That email cannot be used for this account.")
    raw = secrets.token_urlsafe(32)
    db.session.execute(
        db.update(EmailVerificationToken)
        .where(
            EmailVerificationToken.user_id == user.id,
            EmailVerificationToken.used_at.is_(None),
        )
        .values(used_at=utcnow())
    )
    db.session.add(
        EmailVerificationToken(
            user_id=user.id,
            email=email,
            token_hash=token_hash(raw),
            expires_at=utcnow() + timedelta(hours=24),
        )
    )
    audit("email_verification_requested", actor_id=user.id)
    db.session.commit()
    url = current_app.config["APP_BASE_URL"] + "/verify-email?token=" + raw
    queue_mail(
        email,
        "Confirm your JobMatch email",
        f"Confirm this email address for your JobMatch account:\n\n{url}\n\nThis link expires in 24 hours and works once. If you did not request this, ignore this email.\n",
    )


def confirm_email(raw):
    if not isinstance(raw, str) or not 32 <= len(raw) <= 128:
        raise ValidationError("This confirmation link is invalid or expired.")
    token = db.session.scalar(
        db.select(EmailVerificationToken).where(
            EmailVerificationToken.token_hash == token_hash(raw)
        )
    )
    user = db.session.get(User, token.user_id) if token else None
    if (
        not token
        or token.used_at
        or token.expires_at <= utcnow()
        or not user
        or not user.is_active
    ):
        raise ValidationError("This confirmation link is invalid or expired.")
    changed = db.session.execute(
        db.update(EmailVerificationToken)
        .where(
            EmailVerificationToken.id == token.id,
            EmailVerificationToken.used_at.is_(None),
            EmailVerificationToken.expires_at > utcnow(),
        )
        .values(used_at=utcnow())
    ).rowcount
    if not changed:
        db.session.rollback()
        raise ValidationError("This confirmation link is invalid or expired.")
    email_changed = user.email != token.email
    user.email = token.email
    user.email_verified_at = utcnow()
    if email_changed:
        revoke_sessions(user)
        db.session.execute(
            db.update(PasswordResetToken)
            .where(
                PasswordResetToken.user_id == user.id,
                PasswordResetToken.used_at.is_(None),
            )
            .values(used_at=utcnow())
        )
    audit("email_verified", actor_id=user.id)
    try:
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise ValidationError("That email cannot be used for this account.") from exc
    return email_changed
