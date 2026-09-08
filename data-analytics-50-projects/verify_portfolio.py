from pathlib import Path
root=Path(__file__).parent
folders=sorted(p for p in root.iterdir() if p.is_dir() and p.name[:2].isdigit())
assert len(folders)==50, f'Expected 50 projects, found {len(folders)}'
required={'Excel':'workbook_blueprint.md','SQL':'analysis.sql','Python':'analysis.py','Statistics':'analysis.py','Power BI':'measures.dax','Tableau':'calculated_fields.txt'}
counts={k:0 for k in required}
for p in folders:
    text=(p/'README.md').read_text(encoding='utf-8')
    tool=next(k for k in required if f'**Tool:** {k}' in text)
    assert (p/required[tool]).exists(), f'Missing deliverable in {p.name}'
    counts[tool]+=1
assert counts=={'Excel':10,'SQL':10,'Python':10,'Statistics':8,'Power BI':6,'Tableau':6}, counts
print('PASS: 50 complete projects', counts)
