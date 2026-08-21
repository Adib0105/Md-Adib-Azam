# WFH Job Application Agent

A truth-first remote-job discovery and application-preparation system for Md Adib Azam.

## What it does

- Discovers public jobs from supported ATS feeds (initially Greenhouse and Lever).
- Keeps only explicitly remote/WFH jobs when `remote_only` is enabled.
- Scores jobs against resume-backed skills and target titles.
- Rejects obvious payment/deposit and suspicious recruiter patterns.
- Stores every job in SQLite so duplicates are not processed again.
- Provides a Streamlit dashboard with match score, verdict and application URL.
- Includes a Playwright assistant that fills only known basic fields.
- Stops for CAPTCHA, login, salary/notice questions, legal/EEO questions and unknown fields.
- Never invents candidate information.

## Important limitation

There is no universal legitimate API that can submit applications to every employer. Many ATS submission APIs require employer-owned credentials. Browser flows also change frequently. For this reason the default configuration has `allow_auto_submit: false`. The system can discover, rank and prepare applications reliably; submission should only be enabled per supported site after testing its flow and terms.

## Setup

```bash
cd job-application-agent
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp config.example.yaml config.yaml
```

Fill only truthful candidate values in `config.yaml`. Keep that file private.

## Discover jobs

Greenhouse and Lever use company-specific board/site identifiers:

```bash
python agent.py --greenhouse COMPANY_BOARD --lever COMPANY_SITE
```

The agent records results in `jobs.db` and marks them `QUALIFIED`, `REVIEW`, or `SKIP`.

## Dashboard

```bash
streamlit run dashboard.py
```

## Prepare an application

```bash
python apply_assistant.py "https://employer.example/apply"
```

The browser assistant fills only basic fields it can map confidently and then pauses for review. It does **not** click Submit.

## Daily automation

Use Windows Task Scheduler, cron, or GitHub Actions for discovery. Do not put private candidate data or job-board credentials in a public repository. If you later automate a supported application flow, store secrets locally or in encrypted CI secrets.

Suggested production rule:

`Remote India + age <= 7 days + verified source + match >= 75 + max 10/day + no payment + no fabricated answers.`

## Next engineering milestones

1. Employer-domain verification and richer scam scoring.
2. Job-post freshness parsing and 7-day enforcement.
3. More public ATS discovery adapters.
4. Resume variants and JD keyword mapping.
5. Application-question extraction and human-review queue.
6. Per-site tested submission adapters where permitted.
7. Daily email/report and application follow-up tracking.
