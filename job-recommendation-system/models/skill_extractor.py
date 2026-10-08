"""Dictionary NLP with boundary-aware aliases; no downloaded language models."""

import re

SKILL_GROUPS = {
    "Programming": "Python|Java|JavaScript|TypeScript|C++|C#|R|Go|Rust|PHP|Kotlin|Swift|Bash|OOP|Algorithms|Data Structures",
    "Analytics": "SQL|Advanced SQL|Excel|Advanced Excel|Excel VBA|Power BI|Tableau|DAX|Power Query|Statistics|Data Cleaning|Data Visualization|ETL|Pandas|NumPy|Looker|R Programming|A/B Testing|Forecasting|Data Modeling|Reporting|Dashboard Design",
    "Machine Learning": "Machine Learning|Deep Learning|Scikit-learn|TensorFlow|PyTorch|NLP|Computer Vision|Feature Engineering|MLOps|Model Evaluation|Probability|Regression|Clustering|Recommendation Systems|Time Series",
    "Web": "HTML|CSS|React|Angular|Vue|Flask|Django|FastAPI|Node.js|REST API|GraphQL|Bootstrap|Tailwind CSS|Next.js|Express|Accessibility|Web Development",
    "Cloud": "AWS|Azure|Google Cloud|Docker|Kubernetes|Linux|Terraform|CI/CD|Git|GitHub|Jenkins|Networking|Cloud Security|Serverless|Monitoring",
    "Databases": "MySQL|PostgreSQL|SQLite|MongoDB|Redis|Oracle|SQL Server|Snowflake|BigQuery|Spark|Hadoop|Databricks|Database Design",
    "Security": "Cybersecurity|SIEM|SOC|Splunk|Wireshark|Incident Response|Vulnerability Assessment|Penetration Testing|IAM|Risk Assessment|Security Auditing",
    "Marketing": "SEO|SEM|Google Analytics|Google Ads|Meta Ads|Email Marketing|Content Marketing|Social Media|Copywriting|Digital Marketing|Campaign Analysis|Market Research|Conversion Optimization",
    "Design": "Photoshop|Illustrator|Canva|Figma|UI Design|UX Research|Typography|Branding|Video Editing|Premiere Pro|After Effects|InDesign|Prototyping",
    "Business": "Communication|Problem Solving|Teamwork|Leadership|Presentation|Stakeholder Management|Project Management|Agile|Scrum|Jira|Business Analysis|Requirements Gathering|Process Improvement|Negotiation|Time Management",
    "Support": "CRM|Customer Support|Zendesk|Salesforce|Freshdesk|Ticketing|Email Support|Chat Support|Technical Support|Conflict Resolution|Customer Retention|Quality Assurance",
    "Finance and HR": "Financial Modeling|Accounting|Budgeting|Valuation|Tally|SAP|Financial Analysis|Payroll|Recruitment|HR Analytics|HRIS|Compliance|Supply Chain|Inventory Management|Operations|Sales",
}
ALIASES = {
    "ms excel": "Excel",
    "microsoft excel": "Excel",
    "ms-excel": "Excel",
    "powerbi": "Power BI",
    "power-bi": "Power BI",
    "microsoft power bi": "Power BI",
    "scikit learn": "Scikit-learn",
    "sklearn": "Scikit-learn",
    "nodejs": "Node.js",
    "node js": "Node.js",
    "js": "JavaScript",
    "reactjs": "React",
    "react.js": "React",
    "postgres": "PostgreSQL",
    "amazon web services": "AWS",
    "gcp": "Google Cloud",
    "natural language processing": "NLP",
    "search engine optimization": "SEO",
    "customer relationship management": "CRM",
    "adobe photoshop": "Photoshop",
    "adobe illustrator": "Illustrator",
    "ms sql": "SQL Server",
    "communication skills": "Communication",
    "html5": "HTML",
    "css3": "CSS",
    "restful api": "REST API",
    "rest apis": "REST API",
    "data visualisation": "Data Visualization",
    "financial modelling": "Financial Modeling",
    "ml": "Machine Learning",
    "a/b tests": "A/B Testing",
    "vba": "Excel VBA",
}
SKILLS = sorted(
    {s for group in SKILL_GROUPS.values() for s in group.split("|")}, key=str.casefold
)
CANONICAL = {s.casefold(): s for s in SKILLS} | ALIASES
PATTERNS = [
    (re.compile(r"(?<![\w+#])" + re.escape(alias) + r"(?![\w+#])", re.I), skill)
    for alias, skill in sorted(CANONICAL.items(), key=lambda x: -len(x[0]))
    if alias not in {"r", "go"}
]


def normalize_skill(value):
    value = re.sub(r"\s+", " ", str(value or "")).strip()[:100]
    return CANONICAL.get(value.casefold(), value)


def normalize_skills(values):
    if isinstance(values, str):
        values = re.split(r"[,;|\n]", values)
    result = {}
    for value in values or []:
        skill = normalize_skill(value)
        if skill:
            result[skill.casefold()] = skill
    return sorted(result.values(), key=str.casefold)


def ranking_skills(values):
    """Keep concrete tools while recognizing their broader skill family."""
    result = set(normalize_skills(values))
    if result & {"MySQL", "PostgreSQL", "SQL Server", "SQLite", "Advanced SQL"}:
        result.add("SQL")
    if result & {"Advanced Excel", "Excel VBA"}:
        result.add("Excel")
    return sorted(result, key=str.casefold)


def extract_skills(text):
    text = str(text or "")
    found = {skill for pattern, skill in PATTERNS if pattern.search(text)}
    # Ambiguous short words require code-like capitalization or explicit context.
    if re.search(r"(?<!\w)R(?!\w)|\br programming\b", text):
        found.add("R")
    if re.search(r"\b(?:Go programming|Golang|Go language)\b", text, re.I):
        found.add("Go")
    return sorted(found, key=str.casefold)
