"""Public project facts and local FAQ intents. No user data or external services."""

from flask import url_for

COLLEGE_PROJECT = {
    "name": "Job Recommendation",
    "description": (
        "Job Recommendation is an AI/ML-powered career platform that uses NLP, "
        "semantic matching, recommendation models, resume intelligence, skill-gap "
        "analysis and career insights to help users discover relevant job opportunities."
    ),
    "college": "Bengal College of Polytechnic",
    "location": "Durgapur, West Bengal",
    "department": "Department of Computer Science and Technology (CST)",
    "year": "2nd Year",
    "semester": "3rd Semester",
    "session": "2025–2028",
    "submitted_to": "Ardent Computech Pvt. Ltd.",
    "lead": "Md Adib Azam",
    "members": (
        "Sonu Kumar Ram",
        "Raj Koiri",
        "Anurag Prasad",
        "Harleen Kaur Chopra",
        "Amit Kumar Ruidas",
    ),
}

FAQS = (
    {
        "id": "help",
        "question": "What can this chatbot help with?",
        "patterns": [
            r"\b(chatbot|chatgpt|gemini|llm)\b",
            r"^(hi|hello|hey|help|namaste)$",
        ],
        "answer": (
            "I answer local JobMatch FAQs and point you to the right page. "
            "This is an intent-based project guide running in your browser. "
            "It does not use ChatGPT, Gemini or an external LLM, read private "
            "profiles or resumes, or send your chat messages to a server."
        ),
        "links": [("About JobMatch", "public.about", "")],
    },
    {
        "id": "lead",
        "question": "Who is the Head of Group?",
        "patterns": [r"\b(head|lead|leader|adib)\b"],
        "answer": f"{COLLEGE_PROJECT['lead']} is the Head of Group / Project Lead.",
        "links": [("Meet the project team", "public.about", "#project-team")],
    },
    {
        "id": "team",
        "question": "Who are the project team members?",
        "patterns": [r"\b(team|members|group)\b"],
        "answer": (
            f"Head of Group / Project Lead: {COLLEGE_PROJECT['lead']}. "
            "Project team members: " + ", ".join(COLLEGE_PROJECT["members"]) + "."
        ),
        "links": [("Project team", "public.about", "#project-team")],
    },
    {
        "id": "submission",
        "question": "Who was the project submitted to?",
        "patterns": [r"\b(submit\w*|ardent)\b"],
        "answer": f"The Job Recommendation project was submitted to {COLLEGE_PROJECT['submitted_to']}",
        "links": [("College project details", "public.about", "#college-project")],
    },
    {
        "id": "academic",
        "question": "Which year and semester?",
        "patterns": [r"\b(year|semester|session|batch)\b"],
        "answer": (
            f"{COLLEGE_PROJECT['year']} · {COLLEGE_PROJECT['semester']} · "
            f"Session {COLLEGE_PROJECT['session']} · {COLLEGE_PROJECT['department']}."
        ),
        "links": [("College project details", "public.about", "#college-project")],
    },
    {
        "id": "college",
        "question": "Which college is this project from?",
        "patterns": [r"\b(college|department|branch|cst|location|durgapur)\b"],
        "answer": (
            f"{COLLEGE_PROJECT['college']}, {COLLEGE_PROJECT['location']}. "
            f"{COLLEGE_PROJECT['department']}."
        ),
        "links": [("College project details", "public.about", "#college-project")],
    },
    {
        "id": "score",
        "question": "How does the matching score work?",
        "patterns": [r"\b(score|percentage|percent|matching)\b"],
        "answer": (
            "The default hybrid score combines normalized skills, TF-IDF text "
            "similarity and job/profile factors such as role, experience, education, "
            "location and preferences. Unavailable semantic matching is omitted and "
            "the remaining weights are renormalized. Job details show the match "
            "breakdown. A matching percentage ranks fit; it is not a hiring "
            "probability or an ATS guarantee."
        ),
        "links": [("Matching methodology", "recs.methodology", "")],
    },
    {
        "id": "model",
        "question": "What is the ML model used?",
        "patterns": [r"\b(ml|model\w*|algorithm\w*|tfidf|tf idf)\b"],
        "answer": (
            "JobMatch defaults to explainable hybrid matching with scikit-learn "
            "TF-IDF and profile rules; the seven-factor weighted baseline remains "
            "available. Optional Sentence Transformer semantic features require "
            "locally prepared weights. Logistic and Random Forest rankers are "
            "existing experiments and run only when trained and explicitly enabled. "
            "The recorded evaluation uses synthetic data."
        ),
        "links": [("Matching methodology", "recs.methodology", "")],
    },
    {
        "id": "resume",
        "question": "How do I upload my resume?",
        "patterns": [r"\b(resume|cv|upload)\b"],
        "answer": (
            "Sign in, open My profile, and use Choose your resume. Select a text "
            "PDF or DOCX up to 5 MB, then choose Extract & review. Check and correct "
            "the extracted details before confirming. Resume Intelligence explains "
            "the reviewed information. Files are processed locally."
        ),
        "links": [
            ("Upload in My profile", "candidate.profile", "#resume"),
            ("Resume Intelligence", "ml_pages.resume_intelligence", ""),
        ],
    },
    {
        "id": "skills",
        "question": "What is skill gap analysis?",
        "patterns": [r"\b(skill\w*|gap\w*|learning)\b"],
        "answer": (
            "Skill gap analysis compares your reviewed skills with job or target-role "
            "requirements, highlights missing or partial skills and suggests learning "
            "steps. Sign in and open Skill analysis or Career Path to explore it."
        ),
        "links": [
            ("Skill analysis", "recs.skills", ""),
            ("Career Path", "ml_pages.career", ""),
        ],
    },
    {
        "id": "career",
        "question": "What is career intelligence?",
        "patterns": [r"\b(career|intelligence|insights|simulator)\b"],
        "answer": (
            "Career intelligence brings together resume insights, job-fit explanations, "
            "skill gaps and practical career/learning paths. Career insights shows "
            "patterns in the available jobs; Career Path helps you explore a target "
            "role. These are planning aids, not employment guarantees."
        ),
        "links": [
            ("Career insights", "recs.insights", ""),
            ("Career Path", "ml_pages.career", ""),
        ],
    },
    {
        "id": "save",
        "question": "How do I save a job?",
        "patterns": [r"\b(save\w*|bookmark\w*|shortlist)\b"],
        "answer": (
            "Sign in, then choose the bookmark button on a job card or Save job "
            "on its details page. Open Saved jobs to see your shortlist. Use the "
            "bookmark again or Unsave job to remove it."
        ),
        "links": [("Saved jobs", "jobs.saved", "")],
    },
    {
        "id": "tracker",
        "question": "How do I track applications?",
        "patterns": [r"\b(track\w*|application\w*|apply|applied)\b"],
        "answer": (
            "Sign in and choose Add to tracker on a job. In Applications, update "
            "its status and add notes or a follow-up date. This records your own "
            "progress; it does not submit an application to an employer. For real "
            "jobs, Apply on source opens the provider's original listing."
        ),
        "links": [("Applications", "candidate.applications", "")],
    },
    {
        "id": "recommendation",
        "question": "How does job recommendation work?",
        "patterns": [
            r"\brecommend\w*\b.*\b(work\w*|how|kaise|logic)\b",
            r"\b(how|kaise)\b.*\brecommend\w*\b",
            r"^recommendations?$",
        ],
        "answer": (
            "JobMatch compares your reviewed profile with available jobs and ranks "
            "them using the existing hybrid matching pipeline. It explains matching "
            "skills, job-fit factors and gaps. New users receive profile-based matches; "
            "enough job interactions can enable a bounded behavior adjustment. "
            "Complete My profile, then open My recommendations."
        ),
        "links": [
            ("My recommendations", "recs.listing", ""),
            ("My profile", "candidate.profile", ""),
        ],
    },
    {
        "id": "overview",
        "question": "What is JobMatch?",
        "patterns": [r"\b(jobmatch|job recommendation|project|about|overview)\b"],
        "answer": (
            "JobMatch is the Job Recommendation college project: an AI/ML-powered "
            "career platform for relevant job discovery, reviewed resume information, "
            "explainable recommendations, skill gaps and career insights. It also "
            "provides saved jobs and a local application tracker."
        ),
        "links": [
            ("About JobMatch", "public.about", ""),
            ("Explore jobs", "jobs.listing", ""),
        ],
    },
)


def project_faqs():
    """Resolve only fixed application routes; the client never supplies a URL."""
    return [
        {
            **faq,
            "links": [
                {"label": label, "href": url_for(endpoint) + anchor}
                for label, endpoint, anchor in faq["links"]
            ],
        }
        for faq in FAQS
    ]
