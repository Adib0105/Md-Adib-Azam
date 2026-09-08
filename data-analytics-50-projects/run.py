"""Run all 50 analyses or one case; outputs always derive from the original attachment."""
import argparse, html, json
from pathlib import Path
import pandas as pd
import numpy as np
from engine import ROOT,load,database,analyze,fingerprint

def report(p,r):
    display=r.head(25).copy()
    nums=display.select_dtypes(include='number').columns
    display[nums]=display[nums].round(4)
    label='Implemented analysis'
    if p['tool'] in ['Power BI','Tableau']:label='Executed reference analysis + desktop implementation pack (not a native dashboard)'
    content=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(p['title'])}</title>
<style>body{{font:16px system-ui;background:#eef3f8;color:#17243a;margin:0}}main{{max-width:1200px;margin:40px auto;padding:36px;background:white;border-top:8px solid #087e8b;border-radius:12px}}h1{{font-size:32px}}.tag{{color:#087e8b;font-weight:700}}.table{{overflow:auto}}table{{border-collapse:collapse;width:100%;font-size:14px}}th{{background:#142c49;color:white}}th,td{{padding:12px;text-align:left;border-bottom:1px solid #dde5ed}}tbody tr:nth-child(even){{background:#f3f7fa}}.note{{padding:16px;background:#eaf5f3}}a{{color:#086a85}}</style><main>
<div class="tag">SUPERSTORE / {p['tool']} / CASE {p['id']:02d}</div><h1>{html.escape(p['title'])}</h1><p>{html.escape(p['question'])}</p><p class="note">{label}. {len(r):,} output records; preview shows up to 25. Source: 9,994 supplied sales lines. No invented data.</p>
<div class="table">{display.to_html(index=False,escape=True,border=0,na_rep='Not available')}</div>
<p><a href="results.csv">Full results CSV</a> · <a href="README.md">Method and limitations</a> · <a href="../METRIC_DEFINITIONS.md">Metric contract</a></p></main></html>'''
    return content

def run_one(n,d=None,c=None):
    p=next(p for p in json.loads((ROOT/'manifest.json').read_text()) if p['id']==n)
    if d is None:d=load()
    if c is None:c=database(d)
    r=analyze(p,d,c); folder=ROOT/p['folder']
    assert len(r)>0 and len(r.columns)>0, p['title']
    r.to_csv(folder/'results.csv',index=False)
    (folder/'report.html').write_text(report(p,r),encoding='utf-8')
    special=''
    if p['id']==25:
        special=f"Seasonal-naive holdout MAE: {r.seasonal_abs_error.mean():,.2f}; three-month-mean MAE: {r.mean_abs_error.mean():,.2f}. No model tuning on the test period.\n"
    if p['id']==26:special+=f"Outliers flagged: {int(r.outlier_flag.sum())} of {len(r)} orders at the pre-set |robust z| > 3.5 threshold. All scores are retained; no threshold was lowered to manufacture anomalies.\n"
    if p['tool']=='Statistics':special+='Exploratory inference only. Historical sample, repeated customers, skew and non-random assignment limit generalization. See the metric contract for exact assumptions.\n'
    if p['tool'] in ['Power BI','Tableau']:special+='Desktop implementation pack: calculations, precise target output and build instructions are provided. Native PBIX/TWBX creation and desktop execution are NOT verified.\n'
    deliver='[Results](results.csv) · [Readable report](report.html) · [Runner](analysis.py)'
    if p.get('sql'):deliver+=' · [SQL](analysis.sql)'
    if p['tool']=='Excel':deliver+=' · [Excel workbook](analysis.xlsx)\n\n![Workbook preview](dashboard-preview.png)'
    if p['tool'] in ['Power BI','Tableau']:deliver+=' · [Desktop build guide](BUILD.md)'
    sample=r.head(5).round(4).to_csv(index=False)
    method=(f"SQL is in analysis.sql (SQLite dialect); source is loaded automatically by the runner." if p.get('sql') else f"Implementation: ../engine.py, function {'python_analysis' if p.get('python') else 'statistics_analysis'}, branch `{p.get('python',p.get('statistics'))}`. This shared implementation is versioned and auditable.")
    (folder/'README.md').write_text(f'''# {p['id']:02d}. {p['title']}

Tool: **{p['tool']}** | Dataset: [original Superstore CSV](../datasets/source_superstore.csv)

## Business question

{p['question']}

## Run and reproduce

From the collection root:

```bash
python {p['folder']}/analysis.py
```

{deliver}

## Method

{method}

All 9,994 source rows remain available. No unrelated columns are fabricated. [Metric definitions and assumptions](../METRIC_DEFINITIONS.md) apply to every result. Columns in results.csv are the exact implemented metrics, not aspirational KPIs.

## Measured output

Output records: {len(r):,}. First five records:

```csv
{sample}```

{special}
## Decision use and limits

Use the ranked values or estimated effects to prioritize further investigation. These results describe the supplied observation window, not a causal effect or guaranteed future performance. Do not infer churn, stock levels, advertising ROI or delivery SLA from absent data. Compare totals and the independent checks in [verification](../VERIFICATION.json) before interpreting.

## Excel refresh note

For Excel projects, source-derived Input rows are editable and summary formulas recalculate over the current row range. To add source rows or new dimension members, rerun the builder or extend the input/formula ranges and dimension list. These are formula-driven reports, not native PivotTables.
''',encoding='utf-8')
    return r

def all_projects():
    d=load(); c=database(d); ps=json.loads((ROOT/'manifest.json').read_text())
    raw=d.copy()
    for col in ['order_date','ship_date']:raw[col]=raw[col].dt.strftime('%Y-%m-%d')
    raw.to_csv(ROOT/'datasets/superstore_clean.csv',index=False)
    profile=dict(original_filename='Sample - Superstore (1)(2).csv',sha256=fingerprint(),rows=len(d),orders=d.order_id.nunique(),customers=d.customer_id.nunique(),sales=float(d.sales.sum()),profit=float(d.profit.sum()),quantity=int(d.quantity.sum()),margin=float(d.profit.sum()/d.sales.sum()),start=str(d.order_date.min().date()),end=str(d.order_date.max().date()),missing_cells=int(d.isna().sum().sum()),currency='source monetary units; no conversion')
    (ROOT/'DATA_PROFILE.json').write_text(json.dumps(profile,indent=2))
    excel=[]
    for p in ps:
        r=run_one(p['id'],d,c)
        if p['tool']=='Excel':
            excel.append(dict(id=p['id'],title=p['title'],folder=p['folder'],dimension=p['dimension'],rows=d[[p['dimension'],'sales','profit','quantity']].values.tolist(),summary=r.values.tolist()))
        print(f"PASS {p['id']:02d} {p['title']}: {len(r)} rows",flush=True)
    (ROOT/'excel_inputs.json').write_text(json.dumps(excel,ensure_ascii=False))
    rows='\n'.join(f"| {p['id']:02d} | [{p['title']}]({p['folder']}/) | {p['tool']} | {'Desktop implementation pack' if p['tool'] in ['Power BI','Tableau'] else 'Executed analysis' } |" for p in ps)
    (ROOT/'README.md').write_text(f'''# Superstore — 50 Audited Analytics Cases

**Md Adib Azam** · Excel · SQL · Python · Statistics · Power BI · Tableau

Rebuilt entirely from the user-supplied Superstore CSV. Source totals: **{profile['rows']:,} sales lines**, **{profile['orders']:,} orders**, **{profile['customers']:,} customers**, **{profile['sales']:,.2f} Sales**, **{profile['profit']:,.2f} Profit**. Period: {profile['start']} to {profile['end']}.

## Honest deliverables

- 10 actual Excel workbooks: editable input rows, recalculating SUMIF summaries, margins, native charts and formula checks.
- 10 SQL cases: explicit analytical queries run against an automatically loaded SQLite database.
- 10 Python cases: quality, RFM, cohort retention, Pareto, holdout forecast, robust outliers, basket association, shipping quantiles, purchase cadence and loss hotspots.
- 8 statistics cases: full computed outputs with assumptions and limitations.
- 6 Power BI + 6 Tableau cases: executed reference results, measures/calculated fields and specific desktop build instructions. **These 12 are implementation packs, not completed native PBIX/TWBX dashboards.**
- Every case includes a results CSV, a readable HTML report, a business question and a reproducible command.

## Reproduce

```bash
python -m pip install -r requirements.txt
python run.py --all
python verify.py
```

Run any case via its analysis.py. View report.html locally after downloading the repository. Excel binaries are checked in; regeneration requires the documented artifact-tool environment in build_workbooks.mjs, not Python alone.

Original data: [source CSV](datasets/source_superstore.csv) · [provenance](DATA_PROFILE.json) · [definitions](METRIC_DEFINITIONS.md) · [audit](AUDIT_AND_CORRECTIONS.md) · [test evidence](VERIFICATION.json)

## Case index

| # | Case | Track | Status |
|---:|---|---|---|
{rows}

This is a sample-data learning portfolio, not a claim of client work or independently collected real-world data. Statistical findings are exploratory. The original attachment is preserved byte-for-byte; all normalization is in the separate clean file.
''',encoding='utf-8')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--all',action='store_true');parser.add_argument('--project',type=int);a=parser.parse_args()
    if a.all:all_projects()
    elif a.project:run_one(a.project)
    else:parser.error('Choose --all or --project N')
