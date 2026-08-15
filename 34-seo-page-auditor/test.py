from pathlib import Path
from app import audit

good = audit(Path(__file__).with_name("sample_page.html").read_text())
assert good["score"] == 100
bad = audit("<html><head><title>x</title></head><body><h1>A</h1><h1>B</h1><img src='x'></body></html>")
assert bad["score"] <= 40
assert len(bad["issues"]) >= 4
print("SEO auditor tests passed")
