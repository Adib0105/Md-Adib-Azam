"""Create an administrator interactively without a password in shell history."""

import getpass
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from models.database import db, User
from utils.validators import validate_email, validate_password, ValidationError


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reset-existing",
        action="store_true",
        help="Replace an existing administrator's password and revoke its sessions",
    )
    args = parser.parse_args()
    try:
        name = input("Admin name: ").strip()
        email = validate_email(input("Admin email: "))
        password = validate_password(getpass.getpass("Password: "))
        if password != getpass.getpass("Confirm password: "):
            raise ValidationError("Passwords do not match.")
        if not 1 <= len(name) <= 100:
            raise ValidationError("Name must contain 1–100 characters.")
        with create_app().app_context():
            user = db.session.scalar(db.select(User).where(User.email == email))
            if user and (not args.reset_existing or not user.is_admin):
                raise ValidationError(
                    "This email exists. Use --reset-existing for an existing administrator only; candidates are never silently promoted."
                )
            if not user:
                user = User(full_name=name, email=email, is_admin=True)
                db.session.add(user)
            else:
                from services.security_service import revoke_sessions

                revoke_sessions(user)
            user.full_name = name
            user.is_active = True
            user.set_password(password)
            db.session.flush()
            from models.database import (
                PasswordResetToken,
                EmailVerificationToken,
                utcnow,
            )

            for model in (PasswordResetToken, EmailVerificationToken):
                db.session.execute(
                    db.update(model)
                    .where(model.user_id == user.id, model.used_at.is_(None))
                    .values(used_at=utcnow())
                )
            from services.security_service import audit

            audit("admin_bootstrap", actor_id=user.id)
            db.session.commit()
        print(
            "Administrator is ready. Sign in at /admin/login using the password you entered."
        )
    except ValidationError as exc:
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()
