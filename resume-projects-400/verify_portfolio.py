#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
TECH=[f"{i:02d}" for i in range(1,11)]+["16"]
MANUAL=[f"{i:02d}" for i in range(11,16)]

def folders(track:Path)->list[Path]:
    return sorted(p for p in track.iterdir() if p.is_dir() and re.match(r"^\d{2}-",p.name))

def command(args:list[str],cwd:Path)->None:
    subprocess.run(args,cwd=cwd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)

def assert_unique(paths:list[Path])->None:
    hashes={hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    assert len(hashes)==len(paths),f"Duplicate implementations found in {paths[0].parent.parent}"

def main()->None:
    tracks=sorted(p for p in ROOT.iterdir() if p.is_dir() and re.match(r"^\d{2}-",p.name))
    assert len(tracks)==16
    for track in tracks:assert len(folders(track))==25,(track,len(folders(track)))

    python_track=ROOT/"01-python"
    assert_unique([d/"app.py" for d in folders(python_track)])
    for d in folders(python_track):
        command([sys.executable,"-m","unittest","-q","test_app.py"],d)
        command([sys.executable,"app.py"],d)

    c_track=ROOT/"02-c-language";assert_unique([d/"main.c" for d in folders(c_track)])
    if shutil.which("make") and (shutil.which("cc") or shutil.which("gcc")):
        for d in folders(c_track):
            command(["make","-s","clean","all"],d);command([str(d/"app")],d);command(["make","-s","clean"],d)

    java_track=ROOT/"03-java";assert_unique([d/"App.java" for d in folders(java_track)])
    if shutil.which("java"):
        for d in folders(java_track):command(["java","App.java"],d)

    web_track=ROOT/"04-web-development";assert_unique([d/"logic.js" for d in folders(web_track)])
    if shutil.which("node"):
        for d in folders(web_track):command(["node","test.mjs"],d)
    for d in folders(web_track):
        html=(d/"index.html").read_text();assert "<main>" in html and 'type="module"' in html and "aria-live" in html

    wp_track=ROOT/"05-wordpress";shortcodes=set()
    for d in folders(wp_track):
        files=list(d.glob("*.php"));assert len(files)==1
        source=files[0].read_text();assert "defined('ABSPATH')" in source and "add_shortcode" in source and ("sanitize_" in source or "esc_html" in source)
        match=re.search(r"add_shortcode\('([^']+)'",source);assert match and match.group(1) not in shortcodes;shortcodes.add(match.group(1))
        assert source.count("{")==source.count("}")

    sql_track=ROOT/"06-mysql";tables=set()
    for d in folders(sql_track):
        schema=(d/"01-schema.sql").read_text();sample=(d/"02-sample-data.sql").read_text();queries=(d/"03-analytics-queries.sql").read_text()
        assert schema.count("CREATE TABLE IF NOT EXISTS")==2 and "FOREIGN KEY" in schema and "CHECK (" in schema
        found=re.findall(r"CREATE TABLE IF NOT EXISTS (\w+)",schema);assert not tables.intersection(found);tables.update(found)
        assert sample.count("INSERT INTO")==2 and "CREATE OR REPLACE VIEW" in queries
    assert len(tables)==50

    command([sys.executable,"validate_workflows.py"],ROOT/"07-generative-ai")

    analytics=ROOT/"08-data-analytics";assert_unique([d/"analysis.py" for d in folders(analytics)])
    for d in folders(analytics):
        command([sys.executable,"analysis.py"],d)
        assert json.loads((d/"output"/"summary.json").read_text())
        assert (d/"output"/"chart.svg").read_text().startswith("<svg")

    command([sys.executable,"validate_prompts.py"],ROOT/"09-prompt-engineering")

    excel=ROOT/"10-excel-ms-office";xlsx=list(excel.glob("[0-9][0-9]-*/*.xlsx"));assert len(xlsx)==25
    formula_count=0
    for file in xlsx:
        with zipfile.ZipFile(file) as book:
            names=set(book.namelist());assert "[Content_Types].xml" in names and "xl/workbook.xml" in names
            assert any("charts/chart" in name for name in names)
            formula_count+=sum(book.read(name).count(b"<x:f") for name in names if name.startswith("xl/worksheets/sheet"))
    assert formula_count>=900,formula_count

    for number in MANUAL:
        track=next(p for p in tracks if p.name.startswith(number+"-"))
        for d in folders(track):assert [p.name for p in d.iterdir()]==[".gitkeep"],d

    cyber=ROOT/"16-cybersecurity-automation";assert_unique([d/"app.py" for d in folders(cyber)])
    for d in folders(cyber):
        command([sys.executable,"test_app.py"],d);command([sys.executable,"app.py"],d)

    manifest=json.loads((ROOT/"manifest.json").read_text())
    assert manifest["implemented_projects"]==275 and manifest["manual_upload_slots"]==125 and manifest["total_organized_items"]==400
    index=(ROOT/"PROJECT_INDEX.md").read_text();assert len(re.findall(r"^\| \d{3} \|",index,re.M))==400

    for markdown in [ROOT/"README.md",ROOT/"PROJECT_INDEX.md",ROOT.parent/"README.md"]:
        text=markdown.read_text()
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)",text):
            if "://" in target or target.startswith("#"):continue
            assert (markdown.parent/target.split("#",1)[0]).resolve().exists(),(markdown,target)

    print("PASS: 275 implemented projects, 125 clean upload slots, 400 indexed items")
    print("PASS: unique code, tests/builds, SQL integrity, XLSX formulas/charts, output and link checks")

if __name__=="__main__":
    main()
