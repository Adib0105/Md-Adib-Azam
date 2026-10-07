import pytest
from config import validate_weights, RECOMMENDATION_WEIGHTS
from models.database import db, User, Job, RecommendationRun
from models.skill_extractor import normalize_skills, extract_skills
from models.recommendation_model import (
    calculate_skill_score,
    calculate_salary_score,
    calculate_experience_score,
    calculate_education_score,
    calculate_location_score,
)
from services.recommendation_service import (
    engine,
    recommendations,
    active_jobs,
    profile_data,
    snapshot,
)


def test_aliases_and_token_boundaries():
    assert normalize_skills(
        ["MS Excel", "Microsoft Excel", "Excel", "powerbi", "SQL", "sql"]
    ) == ["Excel", "Power BI", "SQL"]
    assert "Java" not in extract_skills("JavaScript developer")
    assert "R" not in extract_skills("reporting software")
    assert "C++" in extract_skills("Experienced in C++ and SQL.")
    assert {"Python", "Power BI", "Excel"} <= set(
        extract_skills("Python, PowerBI and MS Excel")
    )


def test_required_skills_are_weighted_more():
    assert (
        calculate_skill_score(
            ["Python", "SQL", "Power BI"], ["Python", "SQL", "Tableau", "Power BI"]
        )
        == 75
    )
    assert calculate_skill_score(["SQL"], ["SQL"], ["Python"]) == 85
    assert calculate_skill_score(["Python"], ["SQL"], ["Python"]) == 15
    assert calculate_skill_score([], [], []) == 50
    assert calculate_skill_score([], ["SQL"]) == 0


@pytest.mark.parametrize(
    "candidate,minimum,maximum,expected",
    [
        (2, 1, 3, 100),
        (0, 0, 2, 100),
        (1, 3, 5, 100 / 3),
        (None, 2, 4, 50),
        (10, 1, 3, 100),
    ],
)
def test_experience(candidate, minimum, maximum, expected):
    assert calculate_experience_score(candidate, minimum, maximum) == pytest.approx(
        expected
    )


@pytest.mark.parametrize(
    "expected,low,high,score",
    [
        (500000, 450000, 650000, 100),
        (1000000, 400000, 500000, 50),
        (None, 400000, 600000, 50),
        (0, None, None, 50),
    ],
)
def test_salary(expected, low, high, score):
    assert calculate_salary_score(expected, low, high) == score


@pytest.mark.parametrize(
    "degree,required,score",
    [
        ("MTech", "BTech", 100),
        ("B.Tech Computer Science", "Diploma", 100),
        ("Diploma", "BSc", 75),
        ("", "BTech", 50),
        ("BA", "12th", 100),
    ],
)
def test_education(degree, required, score):
    assert calculate_education_score(degree, required) == score


def test_location_preferences_take_precedence():
    assert calculate_location_score("Kolkata / Remote", "Kolkata") == 100
    assert calculate_location_score("Patna", "Remote") == 100
    assert calculate_location_score("Howrah", "Kolkata") == 80
    assert calculate_location_score("Bengaluru", "Bangalore") == 100
    assert calculate_location_score("Remote", "Kolkata", state="West Bengal") == 30
    assert calculate_location_score("Patna", "Pune", relocate=True) == 85


def test_weights_are_validated():
    validate_weights(RECOMMENDATION_WEIGHTS)
    with pytest.raises(ValueError):
        validate_weights({**RECOMMENDATION_WEIGHTS, "skills": 2})
    with pytest.raises(ValueError):
        validate_weights({**RECOMMENDATION_WEIGHTS, "skills": float("nan")})


def test_rank_reproducible_explained_and_cached(app):
    with app.app_context():
        user = db.session.scalar(
            db.select(User).where(User.email == "candidate@example.com")
        )
        rows = recommendations(user)
        count = engine().fit_count
        assert len(rows) == 48
        assert [r["score"] for r in rows] == sorted(
            [r["score"] for r in rows], reverse=True
        )
        assert all(0 <= r["score"] <= 100 and r["reasons"] for r in rows)
        assert rows[0]["score"] == pytest.approx(
            sum(rows[0]["contributions"].values()), abs=0.1
        )
        again = recommendations(user)
        assert [(r["job"].id, r["score"]) for r in rows] == [
            (r["job"].id, r["score"]) for r in again
        ]
        engine().search("remote python", rows)
        recommendations(user)
        assert engine().fit_count == count
        assert (
            "Data" in rows[0]["job"].job_title
            or "Intelligence" in rows[0]["job"].job_title
        )


def test_simulation_does_not_mutate_profile_or_history(app):
    with app.app_context():
        user = db.session.scalar(
            db.select(User).where(User.email == "candidate@example.com")
        )
        before = profile_data(user)
        snapshot(user)
        rows = recommendations(user, extra_skills=["Tableau", "DAX"])
        assert rows and profile_data(user) == before
        assert db.session.scalar(db.select(db.func.count(RecommendationRun.id))) == 1
        active_jobs()[0].views += 1
        db.session.commit()
        assert snapshot(user).id == 1


def test_empty_profile_and_no_jobs(app):
    with app.app_context():
        rows = engine().rank({"skills": []}, active_jobs())
        assert rows and all(r["confidence"] == "Low" for r in rows)
        assert rows[0]["score"] < 40
        assert engine().rank({}, []) == []


def test_job_edit_invalidates_features(app):
    with app.app_context():
        jobs = active_jobs()
        engine().features_for(jobs)
        initial = engine().fit_count
        jobs[0].job_description += " Unusual satellite astronomy data."
        db.session.commit()
        engine().features_for(jobs)
        assert engine().fit_count == initial + 1


def test_unflushed_local_jobs_keep_legacy_score_defaults(app):
    """Offline evaluation uses transient Job objects before ORM defaults are applied."""
    from services.data_service import clean_job_rows, generate_dataset
    from tempfile import TemporaryDirectory
    from pathlib import Path

    with app.app_context(), TemporaryDirectory() as directory:
        raw = generate_dataset(Path(directory) / "jobs.csv", count=1)
        fields = clean_job_rows(raw)[0][0]
        fields["source_id"] = "TRANSIENT-CHECK"
        job = Job(id=1001, **fields)
        profile = {
            "skills": job.required_skills,
            "experience_years": 20,
            "expected_salary": 1,
            "education": "BTech",
            "preferred_role": job.job_title,
        }
        before = engine().rank(profile, [job])[0]["scores"]
        db.session.add(job)
        db.session.commit()
        after = engine().rank(profile, [job])[0]["scores"]
        assert before == after
        assert after["experience"] == 100 and after["salary"] == 100
