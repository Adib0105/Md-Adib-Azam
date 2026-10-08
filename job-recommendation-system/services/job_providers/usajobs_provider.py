from services.job_providers.base import (
    JobProviderBase,
    ProviderError,
    normalize_common,
    plain,
)


class USAJobsProvider(JobProviderBase):
    slug = "usajobs"
    name = "USA Government Jobs"

    @property
    def configured(self):
        return bool(
            self.config.get("USAJOBS_API_KEY") and self.config.get("USAJOBS_USER_AGENT")
        )

    def search_jobs(self, **f):
        if not self.configured:
            raise ProviderError("USAJOBS credentials are not configured.")
        page, count = int(f.get("page", 1)), int(f.get("per_page", 20))
        if not 1 <= page <= 1000 or not 1 <= count <= 50:
            raise ProviderError("Unsupported USAJOBS pagination.")
        params = {"Page": page, "ResultsPerPage": count, "Fields": "full"}
        for key, target in [
            ("q", "Keyword"),
            ("location", "LocationName"),
            ("category", "JobCategoryCode"),
            ("min_salary", "RemunerationMinimumAmount"),
            ("max_salary", "RemunerationMaximumAmount"),
        ]:
            if f.get(key) not in {None, ""}:
                params[target] = f[key]
        if f.get("remote"):
            params["RemoteIndicator"] = "True"
        if f.get("posted") is not None:
            params["DatePosted"] = min(f["posted"], 60)
        if f.get("type") in {"Full-time", "Part-time"}:
            params["PositionScheduleTypeCode"] = (
                "1" if f["type"] == "Full-time" else "2"
            )
        if f.get("sort") in {"newest", "salary"}:
            params.update(
                SortField="opendate" if f["sort"] == "newest" else "salary",
                SortDirection="Desc",
            )
        headers = {
            "Host": "data.usajobs.gov",
            "User-Agent": self.config["USAJOBS_USER_AGENT"],
            "Authorization-Key": self.config["USAJOBS_API_KEY"],
        }
        data = self.transport(
            "https://data.usajobs.gov/api/search", params, headers, self.config
        )
        results = data.get("SearchResult")
        if not isinstance(results, dict) or "SearchResultItems" not in results:
            raise ProviderError("USAJOBS results format was invalid.")
        return self.normalize_results(
            results["SearchResultItems"],
            results.get("SearchResultCountAll", 0),
            remote_search=f.get("remote", False),
        )

    def normalize_job(self, raw, **context):
        data = raw["MatchedObjectDescriptor"]
        details = data.get("UserArea", {}).get("Details", {})
        pay = (data.get("PositionRemuneration") or [{}])[0]
        description = " ".join(
            str(v or "")
            for v in [
                details.get("JobSummary"),
                data.get("QualificationSummary"),
                details.get("MajorDuties"),
                details.get("Requirements"),
            ]
        )
        schedule = (data.get("PositionSchedule") or [{}])[0]
        employment = {"1": "Full-time", "2": "Part-time"}.get(
            str(schedule.get("Code")), "Other"
        )
        remote_value = str(
            details.get("RemoteIndicator", data.get("RemoteIndicator", ""))
        ).lower()
        remote = (
            "remote"
            if remote_value == "true" or context.get("remote_search")
            else "onsite" if remote_value == "false" else "unknown"
        )
        url = (data.get("ApplyURI") or [data.get("PositionURI")])[0]
        category = (data.get("JobCategory") or [{}])[0]
        eligibility = details.get("WhoMayApply", {})
        return normalize_common(
            provider=self.slug,
            source_name=self.name,
            external_id=raw.get("MatchedObjectId"),
            title=data.get("PositionTitle"),
            company=data.get("OrganizationName"),
            description=description,
            location=data.get("PositionLocationDisplay"),
            url=url,
            created=data.get("PublicationStartDate") or data.get("PositionStartDate"),
            deadline=data.get("ApplicationCloseDate") or data.get("PositionEndDate"),
            minimum=pay.get("MinimumRange"),
            maximum=pay.get("MaximumRange"),
            currency="USD",
            period={
                "PA": "year",
                "PH": "hour",
                "PM": "month",
                "PD": "day",
                "PW": "week",
                "BW": "fortnight",
            }.get(pay.get("RateIntervalCode"), "unspecified"),
            employment=employment,
            industry=category.get("Name", "Government"),
            remote=remote,
            education=details.get("Education", ""),
            metadata={
                "control_number": str(raw.get("MatchedObjectId", ""))[:180],
                "position_id": plain(data.get("PositionID"), 180),
                "eligibility": plain(
                    (
                        eligibility.get("Name", "")
                        if isinstance(eligibility, dict)
                        else eligibility
                    ),
                    300,
                ),
                "remote_basis": (
                    "provider remote flag/filter"
                    if remote != "unknown"
                    else "not supplied"
                ),
            },
        )
