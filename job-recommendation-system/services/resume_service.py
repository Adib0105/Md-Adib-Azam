"""Parse uploaded documents in a bounded subprocess, without storing the upload."""

import json
import os
import subprocess
import sys
from pathlib import Path
from flask import current_app
from models.resume_parser import ResumeError, MAX_FILE_BYTES


def parse_resume_isolated(filename, data):
    if not data or len(data) > MAX_FILE_BYTES:
        raise ResumeError("The resume must contain data and be no larger than 5 MB.")
    # Do not pass application secrets/provider credentials to the parsing child.
    environment = {
        key: value
        for key, value in os.environ.items()
        if key in {"PATH", "SYSTEMROOT", "WINDIR", "LANG", "LC_ALL", "LD_LIBRARY_PATH"}
    }
    environment["PYTHONIOENCODING"] = "utf-8"
    try:
        process = subprocess.run(
            [
                sys.executable,
                "-m",
                "ml.preprocessing.resume_worker",
                str(filename)[:500],
            ],
            input=data,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=current_app.config.get("RESUME_PARSE_TIMEOUT", 15),
            cwd=Path(__file__).resolve().parents[1],
            env=environment,
            check=False,
        )
        if process.returncode != 0 or len(process.stdout) > 256 * 1024:
            raise ResumeError(
                "The resume could not be parsed within safe resource limits. Export a simpler text PDF or DOCX."
            )
        result = json.loads(process.stdout)
        if "error" in result:
            raise ResumeError(result["error"])
        return result
    except (subprocess.TimeoutExpired, OSError, ValueError, UnicodeError) as exc:
        if isinstance(exc, ResumeError):
            raise
        raise ResumeError(
            "The resume parser timed out or could not read this document. Export a simpler file."
        ) from None
