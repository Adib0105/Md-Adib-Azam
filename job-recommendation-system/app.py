"""Start locally with `python app.py`, then open http://127.0.0.1:5000."""

import logging
import os
import secrets
from pathlib import Path
from flask import Flask, g, render_template, request, jsonify
from urllib.parse import urlsplit
from flask_wtf.csrf import CSRFProtect
from werkzeug.exceptions import HTTPException
from werkzeug.security import generate_password_hash
from config import Config, ROOT, validate_weights, validate_ml_config
from models.database import db, Job, Notification
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
    if app.config["APP_ENV"] == "production":
        if app.testing or app.debug or len(app.config.get("SECRET_KEY") or "") < 32:
            raise RuntimeError(
                "Production requires a random SECRET_KEY of at least 32 characters and TESTING/DEBUG disabled."
            )
        base = urlsplit(app.config["APP_BASE_URL"])
        if (
            base.scheme != "https"
            or not base.hostname
            or base.username
            or base.password
            or base.query
            or base.fragment
            or base.path not in {"", "/"}
        ):
            raise RuntimeError("Set APP_BASE_URL to your trusted HTTPS site origin.")
        if app.config["MAIL_BACKEND"] in {"file", "memory"} or (
            app.config["MAIL_BACKEND"] == "smtp" and not app.config["MAIL_USE_TLS"]
        ):
            raise RuntimeError(
                "Production mail requires encrypted SMTP or the disabled backend."
            )
        app.config["SESSION_COOKIE_SECURE"] = True
        app.config["TRUSTED_HOSTS"] = [base.hostname]
    if (
        not 1 <= app.config["REAL_JOB_CACHE_TTL_MINUTES"] <= 1440
        or not 100 <= app.config["MAX_RANKING_JOBS"] <= 10000
    ):
        raise RuntimeError(
            "Cache TTL must be 1-1440 minutes and MAX_RANKING_JOBS 100-10000."
        )
    from services.logging_service import configure_logging

    configure_logging(app)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    if not app.config["SECRET_KEY"]:
        if app.config["APP_ENV"] == "production":
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
    validate_ml_config(app.config)
    import models.ml_data as ml_data  # noqa: F401
    from ml.models.embeddings import EmbeddingService
    from ml.models.rankers import RankerRegistry
    from ml.pipelines.hybrid import HybridRecommender

    db.init_app(app)
    CSRFProtect(app)
    app.extensions["recommendation_engine"] = RecommendationEngine()
    app.extensions["embedding_service"] = EmbeddingService(
        app.config, app.instance_path
    )
    app.extensions["ranker_registry"] = RankerRegistry(
        app.instance_path, app.config["ALLOW_SYNTHETIC_RANKER"]
    )
    app.extensions["hybrid_recommender"] = HybridRecommender(
        app.extensions["embedding_service"], app.extensions["ranker_registry"]
    )
    app.extensions["dummy_password_hash"] = generate_password_hash(
        secrets.token_urlsafe(32),
        method=(
            (app.config.get("TEST_PASSWORD_HASH_METHOD") or "scrypt")
            if app.testing
            else "scrypt"
        ),
    )

    from routes.auth import auth
    from routes.candidate import candidate
    from routes.jobs import jobs
    from routes.recommendations import recs
    from routes.admin import admin

    from routes.workspace import workspace
    from routes.control import control, admin_api
    from routes.public import public
    from routes.ml import ml_pages

    for blueprint in [
        auth,
        candidate,
        jobs,
        recs,
        admin,
        workspace,
        control,
        admin_api,
        public,
        ml_pages,
    ]:
        app.register_blueprint(blueprint)

    @app.before_request
    def load_user():
        from services.security_service import load_session_user

        load_session_user()

    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )
        if request.path in {"/reset-password", "/verify-email"}:
            response.headers["Referrer-Policy"] = "no-referrer"
            response.headers["X-Robots-Tag"] = "noindex, nofollow"
        if app.config["APP_ENV"] == "production":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )
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
        from services.settings_service import content
        from services.job_catalog import google_jobs_url

        return {
            "current_user": g.get("user"),
            "site_content": content(),
            "google_jobs_url": google_jobs_url,
            "notification_count": (
                db.session.scalar(
                    db.select(db.func.count(Notification.id)).where(
                        Notification.user_id == g.user.id,
                        Notification.read_at.is_(None),
                    )
                )
                if g.get("user")
                else 0
            ),
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
                429: "Too many requests. Please wait before trying again.",
            }.get(status, error.description)
        else:
            status, message = 500, "Something went wrong. Please try again."
            app.logger.error(
                "request_failed",
                extra={"event": "request_failed", "error_type": type(error).__name__},
            )
        db.session.rollback()
        if request.path.startswith("/api/"):
            return jsonify(error=message), status
        return render_template("error.html", code=status, message=message), status

    @app.get("/health")
    def health():
        try:
            db.session.execute(db.text("SELECT 1"))
            return jsonify(status="ok")
        except Exception:
            db.session.rollback()
            return jsonify(status="unavailable"), 503

    with app.app_context():
        from services.schema_service import upgrade_schema

        upgrade_schema()
        from services.job_providers.provider_registry import initialize_providers

        initialize_providers()
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
            app.extensions["recommendation_engine"].features_for(
                sorted(jobs_data, key=lambda job: job.id)
            )
    return app


if __name__ == "__main__":
    from waitress import serve

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    app = create_app()
    port = int(os.getenv("PORT", "5000"))
    print(f"JobMatch is running on http://127.0.0.1:{port}", flush=True)
    print("Open this address in Google Chrome. Press Ctrl+C to stop.", flush=True)
    serve(app, host="127.0.0.1", port=port, threads=4)
