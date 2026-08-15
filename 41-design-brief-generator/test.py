from app import build_brief

request = {
    "brand": "Example",
    "objective": "Launch a service",
    "audience": "Small businesses",
    "message": "Start today",
    "mood": "premium",
    "channels": ["youtube"],
}
brief = build_brief(request)
assert "# Creative brief — Example" in brief
assert "1280 x 720" in brief
assert "#C9A227" in brief
try:
    build_brief({"brand": "Missing"})
except ValueError:
    pass
else:
    raise AssertionError("Incomplete request should fail")
print("Design brief generator tests passed")
