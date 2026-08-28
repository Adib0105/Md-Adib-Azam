#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,json
from pathlib import Path

ROOT=Path(__file__).parent
spec=importlib.util.spec_from_file_location("runner",ROOT/"workflow_runner.py")
runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
folders=sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name[:2].isdigit())
assert len(folders)==25
prompts=[]
for folder in folders:
    workflow=json.loads((folder/"workflow.json").read_text())
    sample=json.loads((folder/"sample.json").read_text())
    assert set(workflow)=={"title","purpose","required_fields","system_prompt","output_sections"}
    prompt=runner.build_prompt(workflow,sample)
    assert workflow["title"] in prompt and all(section in prompt for section in workflow["output_sections"])
    assert "Do not invent facts" in prompt
    prompts.append(prompt)
assert len(set(prompts))==25
print("PASS: 25 workflows validated; unique prompts, schemas and safety contracts")
