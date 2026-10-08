"""Essential content, navigation and data-isolation checks for the project guide."""

import json
import re
from urllib.parse import urlsplit

from models.database import db, User


def faqs(response):
    page = response.get_data(as_text=True)
    source = re.search(
        r'<script type="application/json" id="project-chat-faqs">(.*?)</script>',
        page,
        re.S,
    )
    assert source
    return json.loads(source.group(1))


def test_about_preserves_page_and_shows_exact_college_team(client):
    response = client.get("/about")
    assert response.status_code == 200
    page = response.get_data(as_text=True)
    for expected in (
        "Job Recommendation",
        "Bengal College of Polytechnic",
        "Durgapur, West Bengal",
        "Department of Computer Science and Technology (CST)",
        "2nd Year",
        "3rd Semester",
        "2025–2028",
        "Ardent Computech Pvt. Ltd.",
        "Md Adib Azam",
        "Head of Group",
        "Project Lead",
        "Sonu Kumar Ram",
        "Raj Koiri",
        "Anurag Prasad",
        "Harleen Kaur Chopra",
        "Amit Kumar Ruidas",
        "Clarity before the next step.",
        "Project overview",
        "HOW RECOMMENDATION WORKS",
    ):
        assert expected in page
    for unrelated in ("Assignment No. 02", "Topic: Python", "Python Assignment"):
        assert unrelated not in page


def test_chat_faqs_are_public_and_independent_of_private_profile(app, client):
    public_faqs = faqs(client.get("/"))
    with app.app_context():
        candidate = db.session.scalar(
            db.select(User).where(User.email == "candidate@example.com")
        )
        candidate.resume_text = "PRIVATE_RESUME_TEST_MARKER"
        candidate.phone = "PRIVATE_PHONE_TEST_MARKER"
        db.session.commit()
    client.post(
        "/login", data={"email": "candidate@example.com", "password": "Testpass123"}
    )
    private_page_faqs = faqs(client.get("/dashboard"))
    assert private_page_faqs == public_faqs
    assert "PRIVATE_RESUME_TEST_MARKER" not in json.dumps(private_page_faqs)
    assert "PRIVATE_PHONE_TEST_MARKER" not in json.dumps(private_page_faqs)
    assert len({item["id"] for item in public_faqs}) == len(public_faqs)


def test_chat_navigation_uses_existing_local_routes_and_keeps_headers(client):
    response = client.get("/about")
    assert "script-src 'self'" in response.headers["Content-Security-Policy"]
    for faq in faqs(response):
        for link in faq["links"]:
            target = urlsplit(link["href"])
            assert link["href"].startswith("/") and not target.netloc
            assert not target.scheme
            assert client.get(target.path).status_code in {200, 302}
    for asset in ("css/project-help.css", "js/project-help.js"):
        assert client.get("/static/" + asset).status_code == 200
