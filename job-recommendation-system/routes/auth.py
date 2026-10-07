import hashlib
import time
from functools import wraps
from flask import (
    Blueprint,
    current_app,
    g,
    session,
    request,
    redirect,
    url_for,
    render_template,
    flash,
    abort,
    jsonify,
)
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from models.database import db, User
from utils.validators import (
    ValidationError,
    validate_email,
    validate_password,
    text_field,
)

auth = Blueprint("auth", __name__)


def login_required(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        if not g.user:
            if request.path.startswith("/api/"):
                return jsonify(error="Login is required."), 401
            return redirect(url_for("auth.login"))
        return function(*args, **kwargs)

    return wrapped


def admin_required(function):
    @wraps(function)
    @login_required
    def wrapped(*args, **kwargs):
        if not g.user.is_admin:
            abort(403)
        return function(*args, **kwargs)

    return wrapped


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            name = text_field(request.form, "full_name", 100, True)
            email = validate_email(request.form.get("email", ""))
            password = validate_password(request.form.get("password", ""))
            if password != request.form.get("confirm_password", ""):
                raise ValidationError("Your passwords do not match.")
            user = User(full_name=name, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
        except ValidationError as exc:
            flash(str(exc), "error")
            return render_template("auth.html", mode="register"), 400
        except IntegrityError:
            db.session.rollback()
            flash("This email is already registered. Please sign in.", "error")
            return render_template("auth.html", mode="register"), 400
        session.clear()
        session["user_id"] = user.id
        session.permanent = True
        flash(
            "Your account is ready. Add your skills to personalize your matches.",
            "success",
        )
        return redirect(url_for("candidate.profile"))
    return render_template("auth.html", mode="register")


def perform_login(admin_mode=False):
    if request.method == "POST":
        email = request.form.get("email", "").strip().casefold()[:254]
        password = request.form.get("password", "")[:129]
        key = hashlib.sha256(
            f"{request.remote_addr}|{email}|{admin_mode}".encode()
        ).hexdigest()
        attempts = current_app.extensions["auth_attempts"]
        now = time.monotonic()
        for stale in [
            k for k, values in attempts.items() if not values or now - values[-1] > 900
        ]:
            attempts.pop(stale, None)
        attempts[key] = [t for t in attempts.get(key, []) if now - t < 900]
        if len(attempts[key]) >= 8:
            abort(429)
        user = db.session.scalar(db.select(User).where(User.email == email))
        valid = check_password_hash(
            user.password_hash
            if user
            else current_app.extensions["dummy_password_hash"],
            password,
        )
        if not user or not valid or user.is_admin != admin_mode:
            attempts[key].append(now)
            flash("Email or password is incorrect for this sign-in page.", "error")
            return render_template(
                "auth.html", mode="admin" if admin_mode else "login"
            ), 401
        attempts.pop(key, None)
        session.clear()
        session["user_id"] = user.id
        session.permanent = True
        return redirect(
            url_for("admin.dashboard" if admin_mode else "candidate.dashboard")
        )
    return render_template("auth.html", mode="admin" if admin_mode else "login")


@auth.route("/login", methods=["GET", "POST"])
def login():
    return perform_login()


@auth.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    return perform_login(True)


@auth.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("candidate.index"))
