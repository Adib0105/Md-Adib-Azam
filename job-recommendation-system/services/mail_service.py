"""SMTP and private development mail. Message bodies are never application logs."""

import os
import smtplib
import ssl
from concurrent.futures import ThreadPoolExecutor
from email.message import EmailMessage
from pathlib import Path
from uuid import uuid4
from flask import current_app


def mail_status():
    config = current_app.config
    backend = config["MAIL_BACKEND"]
    configured = (
        backend in {"file", "memory"}
        and config["APP_ENV"] != "production"
        or backend == "smtp"
        and bool(config["MAIL_SERVER"] and config["MAIL_DEFAULT_SENDER"])
    )
    return {
        "backend": backend,
        "configured": bool(configured),
        "encrypted": config["MAIL_USE_TLS"] if backend == "smtp" else None,
    }


def send_mail(recipient, subject, body):
    config = current_app.config
    backend = config["MAIL_BACKEND"]
    if not mail_status()["configured"]:
        return False
    message = EmailMessage()
    message["From"] = config["MAIL_DEFAULT_SENDER"]
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)
    try:
        if backend == "memory" and current_app.testing:
            current_app.extensions.setdefault("mail_outbox", []).append(message)
        elif backend == "file" and config["APP_ENV"] != "production":
            folder = Path(current_app.instance_path) / "mail"
            folder.mkdir(parents=True, exist_ok=True, mode=0o700)
            fd = os.open(
                folder / (uuid4().hex + ".eml"),
                os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o600,
            )
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(message.as_string())
        elif backend == "smtp":
            context = ssl.create_default_context()
            client_type = (
                smtplib.SMTP_SSL if config["MAIL_PORT"] == 465 else smtplib.SMTP
            )
            options = {"timeout": 10}
            if client_type is smtplib.SMTP_SSL:
                options["context"] = context
            with client_type(
                config["MAIL_SERVER"], config["MAIL_PORT"], **options
            ) as server:
                if config["MAIL_USE_TLS"] and client_type is smtplib.SMTP:
                    server.starttls(context=context)
                if config["MAIL_USERNAME"]:
                    server.login(config["MAIL_USERNAME"], config["MAIL_PASSWORD"])
                server.send_message(message)
        else:
            return False
        current_app.logger.info(
            "mail_sent", extra={"event": "mail_sent", "status": "ok"}
        )
        return True
    except (OSError, smtplib.SMTPException, ValueError):
        current_app.logger.error(
            "mail_delivery_failed", extra={"event": "mail_delivery_failed"}
        )
        return False


def queue_mail(recipient, subject, body):
    app = current_app._get_current_object()
    if not app.config["MAIL_ASYNC"]:
        return send_mail(recipient, subject, body)
    if "mail_executor" not in app.extensions:
        app.extensions["mail_executor"] = ThreadPoolExecutor(
            max_workers=2, thread_name_prefix="jobmatch-mail"
        )

    def deliver():
        with app.app_context():
            success = send_mail(recipient, subject, body)
            if not success:
                from services.security_service import audit
                from models.database import db

                audit(
                    "mail_delivery_failed",
                    details={"backend": app.config["MAIL_BACKEND"]},
                )
                db.session.commit()

    app.extensions["mail_executor"].submit(deliver)
    return True
