"""Guarded browser assistant.

This module deliberately prepares/fills only known fields. It DOES NOT auto-submit by default.
CAPTCHA, authentication, legal attestations, salary questions and unknown fields stop the flow.
"""
from __future__ import annotations

import re
from pathlib import Path
import yaml
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent

SENSITIVE_OR_AMBIGUOUS = re.compile(
    r"salary|compensation|notice|captcha|password|gender|disability|veteran|race|ethnicity|"
    r"work authorization|sponsorship|criminal|background|signature|attest|consent",
    re.I,
)

FIELD_MAP = {
    "name": "name", "full name": "name", "email": "email", "phone": "phone",
    "location": "location", "city": "location",
}


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def label_text(el) -> str:
    try:
        aria = el.get_attribute("aria-label") or ""
        placeholder = el.get_attribute("placeholder") or ""
        name = el.get_attribute("name") or ""
        eid = el.get_attribute("id") or ""
        return " ".join([aria, placeholder, name, eid]).strip()
    except Exception:
        return ""


def prepare(url: str, config_path: str, headless: bool = False):
    cfg = load_config(config_path)
    candidate = cfg["candidate"]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        print(f"Opened: {page.title()}")

        unknown = []
        for el in page.locator("input, textarea").all():
            text = label_text(el)
            if not text or el.get_attribute("type") in {"hidden", "submit", "button", "file"}:
                continue
            if SENSITIVE_OR_AMBIGUOUS.search(text):
                unknown.append(text); continue
            key = next((v for k, v in FIELD_MAP.items() if k in text.lower()), None)
            if key and candidate.get(key):
                try: el.fill(str(candidate[key]))
                except Exception: pass
            else:
                unknown.append(text)

        print("\nPrepared known fields. Review everything in the browser.")
        if unknown:
            print("NEEDS HUMAN REVIEW:")
            for q in sorted(set(unknown)): print(f" - {q}")
        print("\nSUBMISSION IS DISABLED. Close browser when finished reviewing.")
        page.pause()
        browser.close()

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--config", default=str(ROOT / "config.yaml"))
    args = ap.parse_args()
    prepare(args.url, args.config)
