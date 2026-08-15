from __future__ import annotations

import argparse
import json
from pathlib import Path


PALETTES = {
    "professional": ["#12355B", "#2F6690", "#F4F7FA", "#D1495B"],
    "energetic": ["#FF5A36", "#FFB627", "#4ECDC4", "#172A3A"],
    "premium": ["#111111", "#C9A227", "#F7F1E3", "#5C5470"],
    "friendly": ["#5B8DEF", "#6FD08C", "#FFF3B0", "#3D405B"],
}
FORMATS = {
    "instagram": "1080 x 1350 px feed post plus 1080 x 1920 px story",
    "linkedin": "1200 x 1200 px feed post",
    "youtube": "1280 x 720 px thumbnail",
    "print": "A4 print-ready PDF with 3 mm bleed",
}


def build_brief(request: dict[str, object]) -> str:
    required = ["brand", "objective", "audience", "message"]
    missing = [field for field in required if not str(request.get(field, "")).strip()]
    if missing:
        raise ValueError("Missing required fields: " + ", ".join(missing))

    mood = str(request.get("mood", "professional")).lower()
    channels = [str(item).lower() for item in request.get("channels", ["instagram"])]
    palette = PALETTES.get(mood, PALETTES["professional"])
    deliverables = [FORMATS.get(channel, channel + " asset, size to confirm") for channel in channels]
    deadline = request.get("deadline", "To be confirmed")

    lines = [
        f"# Creative brief — {request['brand']}",
        "",
        "## Objective",
        str(request["objective"]),
        "",
        "## Audience",
        str(request["audience"]),
        "",
        "## Core message",
        str(request["message"]),
        "",
        "## Visual direction",
        f"Use a {mood} style with clear hierarchy, strong contrast and accessible typography.",
        "Suggested starting palette: " + ", ".join(palette) + ".",
        "",
        "## Deliverables",
        *[f"- {item}" for item in deliverables],
        "",
        "## Constraints",
        f"- Deadline: {deadline}",
        f"- Call to action: {request.get('call_to_action', 'To be confirmed')}",
        f"- Required text or assets: {request.get('required_assets', 'Logo and approved copy')}",
        "",
        "## Approval questions",
        "- Is the core message accurate?",
        "- Are the audience and call to action approved?",
        "- Are all names, dates, prices and contact details verified?",
        "- Which output sizes are required for final export?",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("request_json", type=Path)
    parser.add_argument("--output", type=Path, default=Path("creative_brief.md"))
    args = parser.parse_args()
    request = json.loads(args.request_json.read_text(encoding="utf-8"))
    brief = build_brief(request)
    args.output.write_text(brief, encoding="utf-8")
    print(f"Saved: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
