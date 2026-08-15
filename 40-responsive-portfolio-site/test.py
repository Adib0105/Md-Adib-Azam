from pathlib import Path

root = Path(__file__).parent
html = (root / "index.html").read_text(encoding="utf-8")
css = (root / "styles.css").read_text(encoding="utf-8")
javascript = (root / "app.js").read_text(encoding="utf-8")
for section in ['id="work"', 'id="skills"', 'id="contact"']:
    assert section in html
assert html.count("data-category=") >= 6
assert "@media" in css
assert "dataset.filter" in javascript
assert "Adib0105" in html
print("Portfolio site checks passed")
