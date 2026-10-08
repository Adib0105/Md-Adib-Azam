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
from flask_wtf.csrf import generate_csrf
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from models.database import db, User, UserSession, AuditLog, utcnow
from services.security_service import audit, rate_limit, start_session
from services.account_service import (
    request_password_reset,
    reset_password,
    change_password,
    request_email_verification,
    confirm_email,
    RESET_RESPONSE,
)
from services.mail_service import mail_status
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
    if g.user and g.user.is_admin:
        return redirect(url_for("admin.dashboard"))
    if request.method == "POST":
        rate_limit("register", 10, 3600)
        try:
            name = text_field(request.form, "full_name", 100, True)
            email = validate_email(request.form.get("email", ""))
            password = validate_password(request.form.get("password", ""))
            if password != request.form.get("confirm_password", ""):
                raise ValidationError("Your passwords do not match.")
            user = User(full_name=name, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.flush()
            audit("account_registered", actor_id=user.id)
            db.session.commit()
        except ValidationError as exc:
            flash(str(exc), "error")
            return render_template("auth.html", mode="register"), 400
        except IntegrityError:
            db.session.rollback()
            flash("This email is already registered. Please sign in.", "error")
            return render_template("auth.html", mode="register"), 400
        start_session(user)
        flash(
            "Your account is ready. Add your skills to personalize your matches.",
            "success",
        )
        return redirect(url_for("candidate.profile"))
    return render_template("auth.html", mode="register")


def perform_login(admin_mode=False):
    if request.method == "POST":
        if g.user and g.user.is_admin and not admin_mode:
            abort(
                403,
                description="Sign out of the administrator workspace before using a candidate account.",
            )
        email = request.form.get("email", "").strip().casefold()[:254]
        password = request.form.get("password", "")[:129]
        rate_limit("login_ip", 40, 900)
        rate_limit("login_identity", 8, 900, f"{email}|{admin_mode}")
        user = db.session.scalar(db.select(User).where(User.email == email))
        valid = check_password_hash(
            (
                user.password_hash
                if user
                else current_app.extensions["dummy_password_hash"]
            ),
            password,
        )
        if not user or not valid or user.is_admin != admin_mode or not user.is_active:
            audit("login_failed", actor_id=user.id if user else None)
            db.session.commit()
            flash("Email or password is incorrect for this sign-in page.", "error")
            return (
                render_template("auth.html", mode="admin" if admin_mode else "login"),
                401,
            )
        start_session(user, request.form.get("remember") == "on")
        audit("admin_login" if admin_mode else "login_succeeded", actor_id=user.id)
        db.session.commit()
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
    if g.get("auth_session"):
        g.auth_session.revoked_at = utcnow()
        audit("logout", actor_id=g.user.id)
        db.session.commit()
    session.clear()
    return redirect(url_for("candidate.index"))


def recovery_payload():
    value = request.get_json(silent=True) if request.is_json else request.form
    if value is None or not hasattr(value, "get"):
        abort(400, description="Send a JSON object or form fields.")
    return value


@auth.route("/forgot-password", methods=["GET", "POST"])
@auth.post("/api/password/forgot")
def forgot_password():
    if request.method == "POST":
        values = recovery_payload()
        email = str(values.get("email", ""))[:254].strip().casefold()
        rate_limit("forgot_ip", 10, 3600)
        rate_limit("forgot_identity", 3, 3600, email)
        request_password_reset(email)
        if request.path.startswith("/api/"):
            return jsonify(message=RESET_RESPONSE)
        flash(RESET_RESPONSE, "success")
    return render_template("account/recovery.html", mode="forgot", token="")


@auth.route("/reset-password", methods=["GET", "POST"])
@auth.post("/api/password/reset")
def reset_password_view():
    token = request.args.get("token", "")[:128]
    if request.method == "POST":
        rate_limit("reset_password", 10, 900)
        values = recovery_payload()
        token = str(values.get("token", ""))[:129]
        try:
            reset_password(
                token,
                str(values.get("password", "")),
                str(values.get("confirm_password", "")),
            )
        except ValidationError as exc:
            if request.path.startswith("/api/"):
                return jsonify(error=str(exc)), 400
            flash(str(exc), "error")
            return (
                render_template("account/recovery.html", mode="reset", token=token),
                400,
            )
        session.clear()
        if request.path.startswith("/api/"):
            return jsonify(message="Password reset. Sign in with your new password.")
        flash("Password reset. All previous sessions have been signed out.", "success")
        return redirect(url_for("auth.login"))
    return render_template("account/recovery.html", mode="reset", token=token)


@auth.get("/api/csrf")
def csrf_token():
    return jsonify(csrf_token=generate_csrf())


@auth.get("/account")
@login_required
def account():
    activity = db.session.scalars(
        db.select(AuditLog)
        .where(AuditLog.actor_id == g.user.id)
        .order_by(AuditLog.id.desc())
        .limit(25)
    ).all()
    sessions = db.session.scalars(
        db.select(UserSession)
        .where(
            UserSession.user_id == g.user.id,
            UserSession.revoked_at.is_(None),
            UserSession.expires_at > utcnow(),
        )
        .order_by(UserSession.id.desc())
        .limit(30)
    ).all()
    return render_template(
        "account/settings.html",
        activity=activity,
        sessions=sessions,
        mail=mail_status(),
    )


@auth.post("/account/password")
@login_required
def update_password():
    rate_limit("change_password", 8, 900, str(g.user.id))
    try:
        change_password(
            g.user,
            request.form.get("current_password", ""),
            request.form.get("password", ""),
            request.form.get("confirm_password", ""),
        )
    except ValidationError as exc:
        flash(str(exc), "error")
        return redirect(url_for("auth.account"))
    session.clear()
    flash(
        "Password changed. Sign in again; previous sessions have been revoked.",
        "success",
    )
    return redirect(url_for("auth.admin_login" if g.user.is_admin else "auth.login"))


@auth.post("/account/email")
@login_required
def update_email():
    rate_limit("verify_email", 3, 3600, str(g.user.id))
    try:
        request_email_verification(
            g.user,
            request.form.get("email", ""),
            request.form.get("current_password", ""),
        )
        flash(
            "Confirmation instructions were requested for that address. Your account email changes only after confirmation.",
            "success",
        )
    except ValidationError as exc:
        flash(str(exc), "error")
    return redirect(url_for("auth.account"))


@auth.route("/verify-email", methods=["GET", "POST"])
def verify_email():
    token = request.args.get("token", "")[:128]
    if request.method == "POST":
        rate_limit("confirm_email", 10, 900)
        try:
            changed = confirm_email(str(request.form.get("token", ""))[:129])
        except ValidationError as exc:
            flash(str(exc), "error")
            return (
                render_template("account/recovery.html", mode="verify", token=""),
                400,
            )
        if changed:
            session.clear()
        flash("Email confirmed. You can now use verified-email alerts.", "success")
        return redirect(url_for("auth.login"))
    return render_template("account/recovery.html", mode="verify", token=token)


@auth.post("/account/sessions/<int:session_id>/revoke")
@login_required
def revoke_session(session_id):
    record = db.session.scalar(
        db.select(UserSession).where(
            UserSession.id == session_id, UserSession.user_id == g.user.id
        )
    )
    if not record:
        abort(404)
    record.revoked_at = utcnow()
    audit("session_revoked", subject_type="session", subject_id=record.id)
    db.session.commit()
    if g.auth_session.id == record.id:
        session.clear()
        return redirect(url_for("auth.login"))
    return redirect(url_for("auth.account"))
