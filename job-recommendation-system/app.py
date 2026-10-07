"""Start locally with `python app.py`, then open http://127.0.0.1:5000."""

import logging
import os
import secrets
from pathlib import Path
from flask import Flask, g, session, render_template, request, jsonify
from flask_wtf.csrf import CSRFProtect
from werkzeug.exceptions import HTTPException
from werkzeug.security import generate_password_hash
from config import Config, ROOT, validate_weights
from models.database import db, User, Job
from services.recommendation_service import RecommendationEngine, active_jobs


def create_app(test_config=None):
    instance_path = (test_config or {}).get(
        "INSTANCE_PATH", os.getenv("JOBMATCH_INSTANCE", str(ROOT / "instance"))
    )
    app = Flask(
        __name__,
        instance_path=str(Path(instance_path).resolve()),
        instance_relative_config=True,
    )
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    if not app.config["SECRET_KEY"]:
        if os.getenv("APP_ENV") == "production":
            raise RuntimeError(
                "Set a long random SECRET_KEY in the environment for production."
            )
        secret_path = Path(app.instance_path) / ".secret.key"
        if not secret_path.exists():
            try:
                fd = os.open(secret_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                with os.fdopen(fd, "w") as handle:
                    handle.write(secrets.token_hex(32))
            except FileExistsError:
                pass
        app.config["SECRET_KEY"] = secret_path.read_text().strip()
    validate_weights(app.config["RECOMMENDATION_WEIGHTS"])
    db.init_app(app)
    CSRFProtect(app)
    app.extensions["recommendation_engine"] = RecommendationEngine()
    app.extensions["dummy_password_hash"] = generate_password_hash(
        secrets.token_urlsafe(32)
    )
    app.extensions["auth_attempts"] = {}

    from routes.auth import auth
    from routes.candidate import candidate
    from routes.jobs import jobs
    from routes.recommendations import recs
    from routes.admin import admin

    for blueprint in [auth, candidate, jobs, recs, admin]:
        app.register_blueprint(blueprint)

    @app.before_request
    def load_user():
        g.user = (
            db.session.get(User, session["user_id"]) if session.get("user_id") else None
        )

    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; "
            "base-uri 'self'; form-action 'self'; frame-ancestors 'none'"
        )
        if not request.path.startswith("/static/"):
            response.headers["Cache-Control"] = "no-store"
        return response

    @app.context_processor
    def shared_context():
        from services.recommendation_service import profile_completion

        return {
            "current_user": g.get("user"),
            "completion": profile_completion(g.user) if g.get("user") else None,
        }

    @app.template_filter("lpa")
    def salary_format(value):
        return "Not listed" if value is None else f"₹{value / 100000:g} LPA"

    @app.template_filter("shortdate")
    def short_date(value):
        return value.strftime("%d %b %Y") if value else "No deadline"

    @app.errorhandler(Exception)
    def handle_error(error):
        if isinstance(error, HTTPException):
            status = error.code
            message = {
                404: "This page could not be found.",
                403: "You do not have access to this page.",
                413: "Your upload is too large. Choose a PDF or DOCX under 5 MB.",
                429: "Too many login attempts. Please wait 15 minutes.",
            }.get(status, error.description)
        else:
            status, message = 500, "Something went wrong. Please try again."
            app.logger.exception("Unhandled request error")
        db.session.rollback()
        if request.path.startswith("/api/"):
            return jsonify(error=message), status
        return render_template("error.html", code=status, message=message), status

    @app.get("/health")
    def health():
        db.session.execute(db.text("SELECT 1"))
        return jsonify(status="ok")

    with app.app_context():
        db.create_all()
        if (
            app.config["SEED_ON_START"]
            and db.session.scalar(db.select(db.func.count(Job.id))) == 0
        ):
            from services.data_service import seed_jobs

            summary = seed_jobs(ROOT / "data")
            if summary["errors"]:
                app.logger.warning(
                    "Skipped %s invalid dataset rows", len(summary["errors"])
                )
        jobs_data = active_jobs()
        if jobs_data:
            app.extensions["recommendation_engine"].features_for(jobs_data)
    return app


if __name__ == "__main__":
    from waitress import serve

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    app = create_app()
    port = int(os.getenv("PORT", "5000"))
    print(f"JobMatch is running on http://127.0.0.1:{port}", flush=True)
    print("Open this address in Google Chrome. Press Ctrl+C to stop.", flush=True)
    serve(app, host="127.0.0.1", port=port, threads=4)
