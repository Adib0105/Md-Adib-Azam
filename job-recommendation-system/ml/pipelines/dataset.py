"""Strict snapshot ingestion, group splitting and reuse of existing job cleaning."""

import hashlib
import json
from datetime import datetime, date, timezone
from pathlib import Path
from sklearn.model_selection import GroupShuffleSplit
from models.database import Job
from services.data_service import clean_job_rows
from ml.preprocessing.text import PROFILE_FIELDS, professional_profile

MAX_DATASET_BYTES = 20 * 1024 * 1024


def utc_timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Dataset timestamps must include a timezone.")
    return parsed.astimezone(timezone.utc)


def load_dataset(path):
    path = Path(path)
    if path.stat().st_size > MAX_DATASET_BYTES:
        raise ValueError("Dataset exceeds the 20 MB limit; use a reviewed partition.")
    contents = path.read_bytes()
    records, seen = [], set()
    candidate_signatures, job_signatures = {}, {}
    for line_number, line in enumerate(contents.decode("utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict) or row.get("schema_version") != "relevance-v1":
            raise ValueError(f"Row {line_number}: incompatible dataset schema.")
        if row.get("dataset_kind") not in {"synthetic", "manual", "behavioral"}:
            raise ValueError(
                f"Row {line_number}: specify synthetic/manual/behavioral provenance."
            )
        candidate = row.get("candidate_features")
        job = row.get("job_features")
        if (
            not isinstance(candidate, dict)
            or not isinstance(job, dict)
            or set(candidate) - PROFILE_FIELDS
        ):
            raise ValueError(
                f"Row {line_number}: only allowlisted professional profile features are accepted."
            )
        if any(
            key in job
            for key in [
                "relevance_label",
                "skill_match",
                "semantic_match",
                "prediction",
            ]
        ):
            raise ValueError(
                "Evaluation labels/predictions cannot be supplied as job features."
            )
        label = row.get("relevance_label")
        if isinstance(label, bool) or not isinstance(label, int) or not 0 <= label <= 3:
            raise ValueError(
                f"Row {line_number}: label must be a reviewed integer from 0 to 3."
            )
        if (
            not isinstance(row.get("candidate_id"), str)
            or not isinstance(row.get("job_id"), str)
            or not row["candidate_id"]
            or not row["job_id"]
        ):
            raise ValueError("Candidate/job IDs must be nonempty pseudonymous strings.")
        if len(row["candidate_id"]) > 100 or len(row["job_id"]) > 100:
            raise ValueError("Dataset IDs are too long.")
        identity = (row["candidate_id"], row["job_id"])
        if identity in seen:
            raise ValueError("Duplicate candidate/job judgments are not allowed.")
        seen.add(identity)
        snapshot = utc_timestamp(row["snapshot_at"])
        # Normalize timezone offsets before deciding what existed at prediction time.
        if date.fromisoformat(job["posted_date"]) > snapshot.date():
            raise ValueError("A job was posted after the candidate snapshot.")
        cutoff = row.get("behavior_cutoff")
        if row["dataset_kind"] == "behavioral" and (
            not cutoff or utc_timestamp(cutoff) > snapshot
        ):
            raise ValueError(
                "Behavioral data needs a cutoff no later than the prediction snapshot."
            )
        judged = utc_timestamp(row["judged_at"]) if row.get("judged_at") else None
        if row["dataset_kind"] == "behavioral" and (
            judged is None or judged < snapshot
        ):
            raise ValueError(
                "Behavioral labels need an explicit observation time at or after the snapshot."
            )
        profile = professional_profile(candidate)
        if not isinstance(candidate.get("skills", []), (list, str)):
            raise ValueError("Candidate skills must be a list or delimited string.")
        for key in ["experience_years", "expected_salary"]:
            value = profile.get(key)
            if value is not None and (
                isinstance(value, bool)
                or not isinstance(value, (float, int))
                or not 0 <= value <= (60 if key == "experience_years" else 100000000)
            ):
                raise ValueError(f"Invalid candidate {key}.")
        for key in PROFILE_FIELDS - {
            "skills",
            "experience_years",
            "expected_salary",
            "willing_to_relocate",
        }:
            if key in profile and (
                not isinstance(profile[key], str) or len(profile[key]) > 12000
            ):
                raise ValueError(f"Invalid candidate {key} text.")
        cleaned, errors = clean_job_rows([job])
        if errors or not cleaned:
            raise ValueError(f"Row {line_number}: invalid job snapshot.")
        fields = cleaned[0]
        if row["dataset_kind"] != "synthetic" and fields["is_synthetic"]:
            raise ValueError(
                "Fixture-derived jobs must be evaluated as synthetic data."
            )
        # Preserve provider uncertainty rather than silently assuming INR/year or known experience.
        for key in ["is_external", "experience_known", "remote_allowed"]:
            if key in job:
                if not isinstance(job[key], bool):
                    raise ValueError(f"Invalid job {key}: expected a boolean.")
                fields[key] = job[key]
        for key, choices in {
            "remote_type": {"remote", "hybrid", "onsite", "unknown"},
            "salary_period": {"year", "month", "week", "day", "hour", "unknown"},
        }.items():
            if key in job:
                if job[key] not in choices:
                    raise ValueError(f"Invalid job {key}.")
                fields[key] = job[key]
        if "salary_currency" in job:
            currency = job["salary_currency"]
            if (
                not isinstance(currency, str)
                or len(currency) != 3
                or not currency.isascii()
                or not currency.isalpha()
            ):
                raise ValueError("Job salary currency must be a three-letter code.")
            fields["salary_currency"] = currency.upper()
        if row["dataset_kind"] != "synthetic":
            fields.setdefault("salary_currency", "UNK")
            fields.setdefault("salary_period", "unknown")
            fields.setdefault("experience_known", False)
            fields.setdefault("is_external", True)
        candidate_signature = json.dumps(
            [profile, snapshot.isoformat()], sort_keys=True
        )
        job_signature = json.dumps(job, sort_keys=True)
        if (
            row["candidate_id"] in candidate_signatures
            and candidate_signatures[row["candidate_id"]] != candidate_signature
        ):
            raise ValueError(
                "Use a distinct candidate snapshot ID when profile or snapshot time changes."
            )
        if (
            row["job_id"] in job_signatures
            and job_signatures[row["job_id"]] != job_signature
        ):
            raise ValueError("Use a distinct job snapshot ID when the listing changes.")
        candidate_signatures[row["candidate_id"]] = candidate_signature
        job_signatures[row["job_id"]] = job_signature
        records.append(
            {
                **row,
                "snapshot_at": snapshot.isoformat(),
                "candidate_features": profile,
                "cleaned_job": fields,
            }
        )
    if len({row["dataset_kind"] for row in records}) > 1:
        raise ValueError(
            "Evaluate synthetic, manual and behavioral datasets separately."
        )
    return records, hashlib.sha256(contents).hexdigest()


def split_dataset(records):
    groups = [row["candidate_id"] for row in records]
    if len(set(groups)) < 4:
        raise ValueError(
            "At least four candidate snapshot groups are needed for a held-out split."
        )
    if records[0]["dataset_kind"] == "behavioral":
        ordered = sorted(
            set(groups),
            key=lambda identity: next(
                utc_timestamp(row["snapshot_at"])
                for row in records
                if row["candidate_id"] == identity
            ),
        )
        test_groups = set(ordered[max(1, int(len(ordered) * 0.75)) :])
        test_start = min(
            utc_timestamp(row["snapshot_at"])
            for row in records
            if row["candidate_id"] in test_groups
        )
        train = [
            i
            for i, row in enumerate(records)
            if row["candidate_id"] not in test_groups
            and utc_timestamp(row["snapshot_at"]) < test_start
            and utc_timestamp(row["judged_at"]) < test_start
        ]
        test = [
            i for i, row in enumerate(records) if row["candidate_id"] in test_groups
        ]
        if not train or not test:
            raise ValueError(
                "Temporal split has no training labels observed before the test window."
            )
        methodology = "Temporal candidate-snapshot split; training labels and snapshots precede the test window. Behavior features are disabled in exported snapshots unless reconstructed by an independently audited event pipeline."
    else:
        train, test = next(
            GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=2026).split(
                records, groups=groups
            )
        )
        train, test = train.tolist(), test.tolist()
        methodology = "Candidate-group held-out 75/25 split (seed 2026); disjoint candidate snapshots, known job catalogue. TF-IDF/role vocabularies fitted only on training job snapshots."
    return [records[i] for i in train], [records[i] for i in test], methodology


def jobs_for(records):
    snapshots = {row["job_id"]: row["cleaned_job"] for row in records}
    return {
        identity: Job(id=index + 1, **fields)
        for index, (identity, fields) in enumerate(sorted(snapshots.items()))
    }


def validate_complete_judgments(records):
    # Unjudged jobs are never treated as negative labels.
    expected = {row["job_id"] for row in records}
    for identity in {row["candidate_id"] for row in records}:
        if {
            row["job_id"] for row in records if row["candidate_id"] == identity
        } != expected:
            raise ValueError(
                "Each evaluated candidate must judge the entire declared job pool; unjudged pairs are not negatives."
            )
