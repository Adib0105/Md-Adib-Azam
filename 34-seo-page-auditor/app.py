from __future__ import annotations

import argparse
import json
from html.parser import HTMLParser
from pathlib import Path


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.title = ""
        self.description = ""
        self.h1_count = 0
        self.images = 0
        self.images_with_alt = 0
        self.links = 0
        self.canonical = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag == "meta" and values.get("name", "").lower() == "description":
            self.description = values.get("content", "") or ""
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "img":
            self.images += 1
            if (values.get("alt") or "").strip():
                self.images_with_alt += 1
        elif tag == "a" and values.get("href"):
            self.links += 1
        elif tag == "link" and values.get("rel", "").lower() == "canonical":
            self.canonical = values.get("href", "") or ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data


def audit(html: str) -> dict[str, object]:
    parser = PageParser()
    parser.feed(html)
    issues = []
    score = 100
    if not (20 <= len(parser.title.strip()) <= 65):
        issues.append("Use a clear title between 20 and 65 characters.")
        score -= 20
    if not (70 <= len(parser.description.strip()) <= 170):
        issues.append("Add a useful meta description between 70 and 170 characters.")
        score -= 20
    if parser.h1_count != 1:
        issues.append("Use exactly one H1 heading.")
        score -= 20
    if parser.images and parser.images_with_alt != parser.images:
        issues.append("Add descriptive alt text to every meaningful image.")
        score -= 20
    if not parser.canonical:
        issues.append("Add a canonical link.")
        score -= 10
    if parser.links == 0:
        issues.append("Add at least one useful internal or external link.")
        score -= 10
    return {
        "score": max(score, 0),
        "title": parser.title.strip(),
        "description_length": len(parser.description.strip()),
        "h1_count": parser.h1_count,
        "images_with_alt": f"{parser.images_with_alt}/{parser.images}",
        "links": parser.links,
        "canonical": parser.canonical,
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("html_file", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.html_file.read_text(encoding="utf-8")), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
