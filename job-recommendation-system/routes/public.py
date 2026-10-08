from flask import Blueprint, render_template, abort
from services.project_faq import COLLEGE_PROJECT

public = Blueprint("public", __name__)


@public.get("/about")
def about():
    return render_template(
        "about.html", public_layout=True, college_project=COLLEGE_PROJECT
    )


@public.get("/info/<page>")
def info(page):
    if page not in {"privacy", "terms", "faq", "contact_details"}:
        abort(404)
    return render_template("info.html", page=page, public_layout=True)
