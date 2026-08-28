#!/usr/bin/env python3
from pathlib import Path
import json,re
ROOT=Path(__file__).parent
folders=sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name[:2].isdigit())
assert len(folders)==25
prompts=[]
for folder in folders:
 text=(folder/"PROMPT.md").read_text()
 cases=json.loads((folder/"eval_cases.json").read_text())
 for heading in ["## System prompt","## Input block","## Procedure","## Output contract","## Guardrails","## Self-evaluation (10 points)"]:assert heading in text
 variables=re.findall(r"- \*\*([a-z_]+)\*\*:",text)
 assert variables and all("input" in c for c in cases)
 assert any(c["expected_behavior"].startswith("Ask") or "refuse" in c["expected_behavior"].lower() or "uncertain" in c["expected_behavior"].lower() for c in cases)
 prompts.append(text)
assert len(set(prompts))==25
print("PASS: 25 unique prompt systems and evaluation packs validated")
