from app import match_resume, tokenize

assert "python" in tokenize("Python and SQL")
result = match_resume(
    "Python SQL Excel dashboards automation customer support",
    "Python SQL Excel dashboards automation support communication cloud",
)
assert 60 <= result["match_score"] <= 90
assert "python" in result["matched_keywords"]
assert "cloud" in result["missing_keywords"]

try:
    match_resume("Python", "and the for")
except ValueError:
    pass
else:
    raise AssertionError("Empty job keywords should be rejected")

print("AI resume matcher tests passed")
