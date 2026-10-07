import json
import logging
from datetime import datetime, timezone


class SafeJSONFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "time": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "event": getattr(record, "event", "application_event"),
        }
        for key in (
            "actor_id",
            "provider",
            "status",
            "duration_ms",
            "count",
            "error_type",
        ):
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        # Raw exception strings, request URLs and arbitrary messages are excluded.
        return json.dumps(payload)


def configure_logging(app):
    handler = logging.StreamHandler()
    handler.setFormatter(SafeJSONFormatter())
    app.logger.handlers = [handler]
    app.logger.setLevel(app.config["LOG_LEVEL"])
    app.logger.propagate = False
