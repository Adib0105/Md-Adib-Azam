import io
import zipfile
import pytest
from pypdf import PdfWriter
from models.resume_parser import parse_resume, ResumeError
from models.database import db, ResumeDraft, User


def test_docx_fields_and_secure_name(resume_docx):
    parsed = parse_resume("../../candidate.docx", resume_docx)
    assert parsed["filename"] == "candidate.docx"
    assert {"SQL", "Python", "Excel", "Power BI"} <= set(parsed["skills"])
    assert parsed["experience_years"] == 1
    assert "B.Tech" in parsed["education"]
    assert "Retail" in parsed["projects"]
    assert "certification" in parsed["certifications"]


@pytest.mark.parametrize(
    "name,data",
    [
        ("file.exe", b"bad"),
        ("fake.pdf", b"not a pdf"),
        ("fake.docx", b"not a zip"),
        ("empty.pdf", b""),
        ("big.pdf", b"x" * (5 * 1024 * 1024 + 1)),
    ],
)
def test_invalid_files(name, data):
    with pytest.raises(ResumeError):
        parse_resume(name, data)


def test_scanned_pdf_is_explained():
    output = io.BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=300, height=300)
    writer.write(output)
    with pytest.raises(ResumeError, match="OCR"):
        parse_resume("scan.pdf", output.getvalue())


def test_readable_pdf_extracts_skills():
    from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject

    writer = PdfWriter()
    page = writer.add_blank_page(width=500, height=500)
    font = DictionaryObject(
        {
            NameObject("/Type"): NameObject("/Font"),
            NameObject("/Subtype"): NameObject("/Type1"),
            NameObject("/BaseFont"): NameObject("/Helvetica"),
        }
    )
    page[NameObject("/Resources")] = DictionaryObject(
        {
            NameObject("/Font"): DictionaryObject(
                {NameObject("/F1"): writer._add_object(font)}
            )
        }
    )
    stream = DecodedStreamObject()
    stream.set_data(
        b"BT /F1 12 Tf 50 450 Td (Data Analyst with Python, SQL, Microsoft Excel and 2 years of experience.) Tj ET"
    )
    page[NameObject("/Contents")] = writer._add_object(stream)
    output = io.BytesIO()
    writer.write(output)
    parsed = parse_resume("resume.pdf", output.getvalue())
    assert {"Python", "SQL", "Excel"} <= set(parsed["skills"])
    assert parsed["experience_years"] == 2


def test_zip_expansion_guard():
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("word/document.xml", "x" * (21 * 1024 * 1024))
    with pytest.raises(ResumeError, match="safe size"):
        parse_resume("bomb.docx", output.getvalue())


def test_resume_review_before_save_and_ownership(app, logged_in, resume_docx):
    result = logged_in.post(
        "/resume/upload", data={"resume": (io.BytesIO(resume_docx), "resume.docx")}
    )
    assert result.status_code == 302
    review_url = result.location
    with app.app_context():
        user = db.session.scalar(
            db.select(User).where(User.email == "candidate@example.com")
        )
        assert not user.resume_text
        assert db.session.scalar(db.select(db.func.count(ResumeDraft.id))) == 1
    assert logged_in.get(review_url).status_code == 200
    outsider = app.test_client()
    outsider.post(
        "/register",
        data={
            "full_name": "Other",
            "email": "other@example.com",
            "password": "Otherpass123",
            "confirm_password": "Otherpass123",
        },
    )
    assert outsider.get(review_url).status_code == 404
    saved = logged_in.post(
        review_url,
        data={
            "action": "confirm",
            "skills": "SQL,Excel",
            "education": "Diploma",
            "experience_years": "0",
            "resume_text": "Reviewed accurate text in my resume.",
            "preferred_role": "MIS Executive",
        },
    )
    assert saved.status_code == 302
    with app.app_context():
        user = db.session.scalar(
            db.select(User).where(User.email == "candidate@example.com")
        )
        assert user.education == "Diploma" and user.experience_years == 0
        assert user.skill_names == ["Excel", "SQL"]
        assert user.resume_filename == "resume.docx"
    assert logged_in.post("/resume/remove").status_code == 302
    with app.app_context():
        assert not db.session.scalar(
            db.select(User).where(User.email == "candidate@example.com")
        ).resume_text
