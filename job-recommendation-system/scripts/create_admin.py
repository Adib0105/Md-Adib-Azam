"""Create an administrator interactively without a password in shell history."""

import getpass
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from models.database import db, User
from utils.validators import validate_email, validate_password, ValidationError


def main():
    try:
        name = input("Admin name: ").strip()
        email = validate_email(input("Admin email: "))
        password = validate_password(getpass.getpass("Password: "))
        if password != getpass.getpass("Confirm password: "):
            raise ValidationError("Passwords do not match.")
        if not 1 <= len(name) <= 100:
            raise ValidationError("Name must contain 1–100 characters.")
        with create_app().app_context():
            if db.session.scalar(db.select(User).where(User.email == email)):
                raise ValidationError(
                    "This email already exists. No account was changed."
                )
            user = User(full_name=name, email=email, is_admin=True)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
        print("Administrator created. Sign in at /admin/login.")
    except ValidationError as exc:
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()
