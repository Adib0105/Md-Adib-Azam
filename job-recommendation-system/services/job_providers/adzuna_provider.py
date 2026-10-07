import re
from services.job_providers.base import (
    JobProviderBase,
    ProviderError,
    normalize_common,
    plain,
)
from services.job_catalog import COUNTRIES, country_currency


class AdzunaProvider(JobProviderBase):
    slug = "adzuna"
    name = "Adzuna"

    @property
    def configured(self):
        return bool(
            self.config.get("ADZUNA_APP_ID") and self.config.get("ADZUNA_APP_KEY")
        )

    def search_jobs(self, **f):
        if not self.configured:
            raise ProviderError("Adzuna credentials are not configured.")
        country = f.get("country", "in")
        page, per_page = int(f.get("page", 1)), int(f.get("per_page", 20))
        if country not in COUNTRIES or not 1 <= page <= 1000 or not 1 <= per_page <= 50:
            raise ProviderError("Unsupported Adzuna country or pagination.")
        params = {
            "app_id": self.config["ADZUNA_APP_ID"],
            "app_key": self.config["ADZUNA_APP_KEY"],
            "results_per_page": per_page,
            "content-type": "application/json",
        }
        for key, target in [
            ("q", "what"),
            ("location", "where"),
            ("category", "category"),
            ("min_salary", "salary_min"),
            ("max_salary", "salary_max"),
        ]:
            if f.get(key) not in {None, ""}:
                params[target] = f[key]
        if f.get("sort") in {"salary", "newest"}:
            params["sort_by"] = "date" if f["sort"] == "newest" else "salary"
            params["sort_dir"] = "down"
        if f.get("posted") is not None:
            params["max_days_old"] = f["posted"]
        field = {
            "Full-time": "full_time",
            "Part-time": "part_time",
            "Contract": "contract",
            "Permanent": "permanent",
        }.get(f.get("type"))
        if field:
            params[field] = 1
        data = self.transport(
            f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}",
            params,
            {},
            self.config,
        )
        if "results" not in data:
            raise ProviderError("Adzuna results format was invalid.")
        return self.normalize_results(
            data["results"], data.get("count", 0), country=country
        )

    def normalize_job(self, raw, **context):
        location = raw.get("location", {}).get("display_name", "")
        # Adzuna has no universal remote filter in this adapter. Only explicit
        # title/location wording is recognized; the UI explains this limitation.
        wording = plain(str(raw.get("title", "")) + " " + str(location))
        remote = (
            "remote"
            if re.search(r"\b(?:remote|work from home)\b", wording, re.I)
            else "hybrid"
            if re.search(r"\bhybrid\b", wording, re.I)
            else "unknown"
        )
        employment = {"full_time": "Full-time", "part_time": "Part-time"}.get(
            raw.get("contract_time"),
            {"contract": "Contract", "permanent": "Permanent"}.get(
                raw.get("contract_type"), "Other"
            ),
        )
        return normalize_common(
            provider=self.slug,
            source_name=self.name,
            external_id=raw.get("id"),
            title=raw.get("title"),
            company=raw.get("company", {}).get("display_name"),
            description=raw.get("description"),
            location=location,
            url=raw.get("redirect_url"),
            created=raw.get("created"),
            minimum=raw.get("salary_min"),
            maximum=raw.get("salary_max"),
            currency=country_currency(context.get("country", "in")),
            employment=employment,
            industry=raw.get("category", {}).get("label", "Other"),
            remote=remote,
            metadata={
                "id": str(raw.get("id", ""))[:180],
                "country": context.get("country", "in"),
                "category": plain(raw.get("category", {}).get("tag", ""), 80),
                "salary_is_predicted": str(raw.get("salary_is_predicted", "0")) == "1",
                "description_is_snippet": True,
                "remote_basis": "explicit title/location wording"
                if remote != "unknown"
                else "not supplied",
            },
        )
