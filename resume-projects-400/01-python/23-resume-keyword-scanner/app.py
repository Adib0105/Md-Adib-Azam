#!/usr/bin/env python3
"""Resume Keyword Scanner - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    import re
    normalize=lambda s:set(re.findall(r"[a-z][a-z0-9+#.-]{1,}",s.lower()))
    resume=normalize(data["resume"]); required=[x.lower() for x in data["required"]]; preferred=[x.lower() for x in data.get("preferred",[])]
    matched_r=[x for x in required if x in resume]; matched_p=[x for x in preferred if x in resume]
    score=100*(0.8*len(matched_r)/max(len(required),1)+0.2*len(matched_p)/max(len(preferred),1)) if preferred else 100*len(matched_r)/max(len(required),1)
    return {"match_score":round(score,1),"matched_required":matched_r,"missing_required":[x for x in required if x not in resume],"matched_preferred":matched_p}


def main() -> None:
    parser = argparse.ArgumentParser(description='Resume Keyword Scanner')
    parser.add_argument("--input", type=Path, default=Path('sample.json'))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = solve(json.loads(args.input.read_text(encoding="utf-8")))
    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
