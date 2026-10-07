from datetime import timedelta
from urllib.error import URLError
import pytest
from models.database import (
    db,
    Job,
    JobProvider,
    ExternalJobCache,
    ExternalJobIdentity,
    utcnow,
)
from services.job_providers.adzuna_provider import AdzunaProvider
from services.job_providers.usajobs_provider import USAJobsProvider
from services.job_providers.base import ProviderError, fetch_json, NoRedirect
from services.external_jobs_service import live_search, upsert_jobs
from services.job_catalog import parse_filters
from services.recommendation_service import recommendations
from utils.validators import safe_external_url, ValidationError


def adzuna_row(**extra):
    return {
        "id": "fixture-101",
        "title": "<b>Remote Python Analyst</b>",
        "company": {"display_name": "Fixture Research"},
        "description": "Build SQL and Python reports. <script>unsafe()</script>",
        "location": {"display_name": "Remote"},
        "redirect_url": "https://www.adzuna.com/details/101?app_key=discard&campaign=test",
        "created": utcnow().isoformat() + "Z",
        "salary_min": 450000,
        "salary_max": 650000,
        "contract_time": "full_time",
        "category": {"label": "IT", "tag": "it-jobs"},
        **extra,
    }


def fake_provider(app, fail=False):
    calls = []
    config = {
        **app.config,
        "ADZUNA_APP_ID": "fixture-id",
        "ADZUNA_APP_KEY": "fixture-secret",
    }

    def transport(url, params, headers, settings):
        calls.append((url, params, headers))
        if fail:
            raise ProviderError("Provider request failed.")
        return {"results": [adzuna_row()], "count": 1}

    provider = AdzunaProvider(config, transport=transport)
    app.extensions["provider_overrides"] = {"adzuna": provider}
    return provider, calls


def test_adzuna_normalization_mapping_and_remote_evidence(app):
    provider, calls = fake_provider(app)
    result = provider.search_jobs(
        q="Python",
        location="Remote",
        country="in",
        sort="salary",
        type="Full-time",
        per_page=10,
    )
    job = result.jobs[0]
    assert (
        job["job_title"] == "Remote Python Analyst"
        and "<" not in job["job_description"]
    )
    assert job["remote_allowed"] and not job["experience_known"]
    assert job["salary_currency"] == "INR" and not job["is_synthetic"]
    assert "app_key" not in job["source_url"]
    assert calls[0][0] == "https://api.adzuna.com/v1/api/jobs/in/search/1"
    assert calls[0][1]["what"] == "Python" and calls[0][1]["full_time"] == 1
    assert calls[0][1]["sort_by"] == "salary"
    assert (
        provider.normalize_job(
            adzuna_row(
                title="Analyst",
                location={"display_name": "Kolkata"},
                description="Not a remote role",
            )
        )["remote_type"]
        == "unknown"
    )


def test_usajobs_mapping_unknowns_and_pay_period(app):
    calls = []
    row = {
        "MatchedObjectId": "gov-101",
        "MatchedObjectDescriptor": {
            "PositionTitle": "Data Analyst",
            "OrganizationName": "Fixture Department",
            "PositionLocationDisplay": "Washington, DC",
            "PositionURI": "https://www.usajobs.gov/job/101",
            "ApplyURI": ["https://www.usajobs.gov/job/101"],
            "PublicationStartDate": utcnow().isoformat(),
            "ApplicationCloseDate": (utcnow() + timedelta(days=7)).isoformat(),
            "PositionRemuneration": [
                {"MinimumRange": "40", "MaximumRange": "50", "RateIntervalCode": "PH"}
            ],
            "PositionSchedule": [{"Code": "1"}],
            "UserArea": {
                "Details": {
                    "JobSummary": "Use Python and SQL.",
                    "WhoMayApply": {"Name": "Check eligibility on source"},
                }
            },
        },
    }

    def transport(url, params, headers, config):
        calls.append((url, params, headers))
        return {"SearchResult": {"SearchResultItems": [row], "SearchResultCountAll": 1}}

    p = USAJobsProvider(
        {
            **app.config,
            "USAJOBS_API_KEY": "fixture-key",
            "USAJOBS_USER_AGENT": "fixture@example.com",
        },
        transport=transport,
    )
    r = p.search_jobs(
        q="data", remote=True, sort="newest", posted=100, type="Part-time"
    )
    job = r.jobs[0]
    assert job["salary_currency"] == "USD" and job["salary_period"] == "hour"
    assert job["remote_allowed"] and job["source_name"] == "USA Government Jobs"
    assert job["experience_known"] is False
    assert calls[0][1]["RemoteIndicator"] == "True" and calls[0][1]["DatePosted"] == 60
    assert calls[0][2]["Authorization-Key"] == "fixture-key"


def test_cache_ttl_dedup_fallback_and_safe_api(app, client):
    provider, calls = fake_provider(app)
    url = "/api/jobs/live?q=Python&provider=adzuna"
    first = client.get(url)
    assert (
        first.status_code == 200
        and first.json["status"] == "live"
        and len(first.json["items"]) == 1
    )
    text = first.get_data(as_text=True)
    assert (
        "fixture-secret" not in text
        and "raw_source_data" not in text
        and "app_key" not in text
    )
    assert client.get(url).json["status"] == "cached" and len(calls) == 1
    with app.app_context():
        cache = db.session.scalar(db.select(ExternalJobCache))
        cache.expires_at = utcnow() - timedelta(seconds=1)
        db.session.commit()
    client.get(url)
    assert len(calls) == 2
    with app.app_context():
        assert (
            db.session.scalar(
                db.select(db.func.count(Job.id)).where(Job.is_external.is_(True))
            )
            == 1
        )
        cache = db.session.scalar(db.select(ExternalJobCache))
        cache.expires_at = utcnow() - timedelta(seconds=1)
        db.session.commit()
    fake_provider(app, fail=True)
    stale = client.get(url).json
    assert (
        stale["status"] == "stale"
        and len(stale["items"]) == 1
        and not stale["fallback"]
    )
    assert "Live refresh unavailable" in stale["message"]


def test_cross_provider_fingerprint_and_identity(app):
    provider, _ = fake_provider(app)
    with app.app_context():
        first = provider.normalize_job(adzuna_row())
        ids, _ = upsert_jobs("adzuna", [first, first])
        second = {
            **first,
            "source": "usajobs",
            "source_name": "USA Government Jobs",
            "external_id": "gov-2",
        }
        other, _ = upsert_jobs("usajobs", [second])
        db.session.commit()
        assert ids == other and len(ids) == 1
        assert db.session.scalar(db.select(db.func.count(ExternalJobIdentity.id))) == 2
        assert db.session.get(Job, ids[0]).source == "adzuna"
        changed = {**first, "job_description": "Changed description"}
        upsert_jobs("adzuna", [changed])
        db.session.commit()
        assert db.session.get(Job, ids[0]).job_description == "Changed description"


def test_lease_budget_missing_credentials_and_malformed(app, client):
    missing = client.get("/api/jobs/live").json
    assert missing["status"] == "unavailable" and missing["fallback"]
    assert all(j["is_synthetic"] for j in missing["items"])
    provider, calls = fake_provider(app)
    with app.app_context():
        live_search("adzuna", parse_filters({}))
        cache = db.session.scalar(db.select(ExternalJobCache))
        cache.expires_at = utcnow() - timedelta(seconds=1)
        cache.lock_until = utcnow() + timedelta(minutes=1)
        db.session.commit()
        assert live_search("adzuna", parse_filters({}))["status"] == "refreshing"
        assert len(calls) == 1
        assert (
            provider.normalize_results(
                [{}, None, adzuna_row(redirect_url="javascript:alert(1)")], 3
            ).skipped
            == 3
        )
        cache.lock_until = None
        app.config["PROVIDER_REQUESTS_PER_HOUR"] = 0
        db.session.commit()
        assert live_search("adzuna", parse_filters({}), force=True)["status"] == "stale"
        assert len(calls) == 1


def test_stale_exclusion_currency_unknown_experience(app, logged_in):
    provider, _ = fake_provider(app)
    with app.app_context():
        fields = provider.normalize_job(adzuna_row())
        fields.update(salary_currency="USD", salary_period="hour")
        ids, _ = upsert_jobs("adzuna", [fields])
        db.session.commit()
        from models.database import User

        job = db.session.get(Job, ids[0])
        user = db.session.get(User, 1)
        row = recommendations(user, jobs=[job])[0]
        assert row["scores"]["salary"] == 50 and row["scores"]["experience"] == 50
        assert row["scores"]["education"] == 50
        assert "USD" in job.salary_display and "LPA" not in job.salary_display
        assert job.freshness == "Fresh"
        job.last_synced_at = utcnow() - timedelta(days=15)
        db.session.commit()
        job_id = job.id
    assert logged_in.get("/api/jobs?source=external").json["total"] == 0
    assert logged_in.post(f"/jobs/{job_id}/apply").status_code == 400
    assert "Apply on Adzuna" not in logged_in.get(f"/jobs/{job_id}").get_data(
        as_text=True
    )


@pytest.mark.parametrize(
    "query",
    [
        "source=unknown",
        "country=xx",
        "remote=maybe",
        "page=-1",
        "page=1.5",
        "per_page=1000",
        "min_salary=nan",
        "min_salary=200&max_salary=1",
        "type=unknown",
        "sort=unknown",
    ],
)
def test_search_input_validation(client, query):
    assert client.get("/api/jobs?" + query).status_code == 400
    assert client.get("/api/jobs/live?" + query).status_code == 400


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        "data:text/html,x",
        "https://localhost/x",
        "http://127.0.0.1/x",
        "https://user:pass@example.com",
        "https://example.com:9000",
        "https://example.com\\evil",
        "https://example.com/\nheader",
    ],
)
def test_unsafe_source_urls(url):
    with pytest.raises(ValidationError):
        safe_external_url(url, required=True)


def test_network_timeout_size_json_and_redirect(app, monkeypatch):
    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self, limit):
            return b"x" * limit

    class Opener:
        def open(self, *args, **kwargs):
            return Response()

    monkeypatch.setattr(
        "services.job_providers.base.build_opener", lambda *args: Opener()
    )
    with pytest.raises(ProviderError, match="size limit"):
        fetch_json("https://api.adzuna.com", {}, {}, {"PROVIDER_MAX_RESPONSE_BYTES": 5})
    Response.read = lambda self, limit: b"not json"
    with pytest.raises(ProviderError, match="invalid JSON"):
        fetch_json("https://api.adzuna.com", {}, {}, app.config)

    def fail(*args, **kwargs):
        raise URLError("secret-bearing-url")

    Opener.open = fail
    with pytest.raises(ProviderError) as exc:
        fetch_json("https://api.adzuna.com", {}, {}, app.config)
    assert "secret-bearing-url" not in str(exc.value)
    with pytest.raises(ProviderError, match="redirect refused"):
        NoRedirect().redirect_request(None, None, 302, "", {}, "https://evil.example")


def test_usajobs_failure_falls_back_without_leaking_key(app, client):
    def fail(*args, **kwargs):
        raise ProviderError("Provider returned HTTP 429.")

    provider = USAJobsProvider(
        {
            **app.config,
            "USAJOBS_API_KEY": "fixture-secret-not-public",
            "USAJOBS_USER_AGENT": "fixture@example.com",
        },
        transport=fail,
    )
    app.extensions["provider_overrides"] = {"usajobs": provider}
    with app.app_context():
        db.session.get(JobProvider, "usajobs").enabled = True
        db.session.commit()
    response = client.get("/api/jobs/live?provider=usajobs")
    assert response.status_code == 200 and response.json["fallback"]
    assert "fixture-secret-not-public" not in response.get_data(as_text=True)
    assert response.json["status"] == "stale"


def test_simultaneous_search_uses_one_http_call(tmp_path):
    import threading
    from concurrent.futures import ThreadPoolExecutor
    from app import create_app

    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "concurrency-fixture",
            "TEST_PASSWORD_HASH_METHOD": "pbkdf2:sha256:1000",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///"
            + str(tmp_path / "concurrent.sqlite"),
            "INSTANCE_PATH": str(tmp_path / "instance"),
            "MODEL_CACHE": False,
            "SEED_ON_START": False,
        }
    )
    entered = threading.Event()
    release = threading.Event()
    calls = []

    def transport(*args):
        calls.append(1)
        entered.set()
        assert release.wait(5)
        return {"results": [adzuna_row()], "count": 1}

    app.extensions["provider_overrides"] = {
        "adzuna": AdzunaProvider(
            {**app.config, "ADZUNA_APP_ID": "fixture", "ADZUNA_APP_KEY": "fixture"},
            transport=transport,
        )
    }

    def query():
        with app.app_context():
            return live_search("adzuna", parse_filters({"q": "python"}))

    with ThreadPoolExecutor(max_workers=2) as executor:
        first = executor.submit(query)
        assert entered.wait(5)
        try:
            second = executor.submit(query).result(timeout=5)
            assert second["status"] == "refreshing" and len(calls) == 1
        finally:
            release.set()
        assert first.result(timeout=5)["status"] == "live"
    with app.app_context():
        db.session.remove()
        db.engine.dispose()
