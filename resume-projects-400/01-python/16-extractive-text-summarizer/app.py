#!/usr/bin/env python3
"""Extractive Text Summarizer - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    import re, collections
    text=data["text"]; sentences=re.split(r'(?<=[.!?])\s+',text.strip())
    stop={"the","a","an","is","are","of","to","and","in","for","with"}
    words=[w.lower() for w in re.findall(r"[A-Za-z']+",text) if w.lower() not in stop]
    freq=collections.Counter(words)
    ranked=sorted(enumerate(sentences),key=lambda x:sum(freq[w.lower()] for w in re.findall(r"[A-Za-z']+",x[1])),reverse=True)
    keep=sorted(ranked[:data.get("sentences",2)])
    return {"summary":" ".join(s for _,s in keep),"original_sentences":len(sentences)}


def main() -> None:
    parser = argparse.ArgumentParser(description='Extractive Text Summarizer')
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
