"""Independent aggregate checks, saved-result reconciliation and workbook package inspection."""
import json, math, zipfile, xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
from engine import ROOT, load, database, orders, analyze, fingerprint

def verify():
    d=load();c=database(d);o=orders(d);ps=json.loads((ROOT/'manifest.json').read_text());checks=[]
    assert len(ps)==50 and len({p['folder'] for p in ps})==50
    assert math.isclose(d.sales.sum(),2297200.8603,abs_tol=1e-7)
    assert math.isclose(d.profit.sum(),286397.0217,abs_tol=1e-7)
    assert len(o)==5009 and d.customer_id.nunique()==793 and d.quantity.sum()==37873
    assert len(d.order_month.unique())==48
    for p in ps:
        r=analyze(p,d,c); saved=pd.read_csv(ROOT/p['folder']/'results.csv',dtype={col:str for col in r.select_dtypes('object').columns},keep_default_na=False,na_values=[''])
        pd.testing.assert_frame_equal(r.reset_index(drop=True),saved,check_dtype=False,check_exact=False,rtol=1e-9,atol=1e-8)
        if p['tool']=='Excel':
            independent=d.groupby(p['dimension'],sort=True).agg(sales=('sales','sum'),profit=('profit','sum'),quantity=('quantity','sum')).reset_index()
            np.testing.assert_allclose(r[['sales','profit','quantity']],independent[['sales','profit','quantity']],rtol=1e-10,atol=1e-7)
            np.testing.assert_allclose(r.margin,r.profit/r.sales,rtol=1e-10)
        checks.append({'id':p['id'],'output_rows':len(r),'rerun_matches_saved':True})
    # Cross-method checks on distinct order aggregation and shipping grain.
    s11=pd.read_csv(ROOT/ps[10]['folder']/'results.csv').sort_values('order_id')
    np.testing.assert_allclose(s11.order_sales,o.sort_values('order_id').sales,rtol=1e-10)
    s18=pd.read_csv(ROOT/ps[17]['folder']/'results.csv').set_index('ship_mode').sort_index()
    py28=pd.read_csv(ROOT/ps[27]['folder']/'results.csv').set_index('ship_mode').sort_index()
    np.testing.assert_allclose(s18.mean_days,py28.mean_days)
    s19=pd.read_csv(ROOT/ps[18]['folder']/'results.csv');assert len(s19)==int((o.profit<0).sum())
    s13=pd.read_csv(ROOT/ps[12]['folder']/'results.csv');assert pd.isna(s13.yoy_growth.iloc[0])
    np.testing.assert_allclose(s13.yoy_growth.iloc[1:],s13.sales.pct_change().iloc[1:])
    rfm=pd.read_csv(ROOT/ps[21]['folder']/'results.csv'); assert len(rfm)==793 and rfm.rfm_sum.between(3,15).all()
    retention=pd.read_csv(ROOT/ps[22]['folder']/'results.csv');assert retention.retention.between(0,1).all();assert (retention.query('year_offset==0').retention==1).all()
    forecast=pd.read_csv(ROOT/ps[24]['folder']/'results.csv');assert len(forecast)==12
    np.testing.assert_allclose(forecast.seasonal_abs_error,abs(forecast.actual_sales-forecast.seasonal_naive))
    for p in ps[30:38]:
        r=pd.read_csv(ROOT/p['folder']/'results.csv')
        assert np.isfinite(r.select_dtypes('number')).all().all()
        if 'p_value' in r:assert r.p_value.between(0,1).all()
        if 'lower_95' in r:assert (r.lower_95<=r.upper_95).all()
    workbook_results=[];ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    for p in ps[:10]:
        path=ROOT/p['folder']/'analysis.xlsx'
        assert path.exists(), f'Missing workbook: {path}'
        with zipfile.ZipFile(path) as z:
            formula_count=0
            for n in z.namelist():
                if n.startswith('xl/worksheets/sheet') and n.endswith('.xml'):
                    doc=ET.fromstring(z.read(n));formula_count+=len(doc.findall('.//s:f',ns));assert not doc.findall('.//s:c[@t="e"]',ns)
            assert formula_count>10;assert any('/charts/chart' in n and n.endswith('.xml') for n in z.namelist())
            sheet=ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
            for cell,expected in [('A8',d.sales.sum()),('B8',d.profit.sum()),('C8',d.quantity.sum()),('D8',d.profit.sum()/d.sales.sum())]:
                actual=sheet.find(f'.//s:c[@r="{cell}"]/s:v',ns)
                assert actual is not None and actual.text is not None, f'Missing cached result {cell}'
                assert math.isclose(float(actual.text),expected,rel_tol=1e-9,abs_tol=1e-6)
        workbook_results.append({'id':p['id'],'formulas':formula_count,'native_chart':True,'cell_errors':0})
    import re
    for path in ROOT.rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if target.startswith(('http','mailto:','#')):continue
            assert (path.parent/target.split('#')[0]).exists(),f'Broken link: {path.name} -> {target}'
    result={'status':'PASS','source_sha256':fingerprint(),'cases':checks,'independent_checks':['10 grouped SQL vs pandas totals and margins','SQL vs pandas order totals','SQL vs Python shipping grain','loss-order population','YoY first-period null','RFM score bounds','cohort retention bounds','holdout absolute errors','statistics finite values and intervals','internal Markdown links','cached XLSX KPI values vs source'],'excel_workbooks':workbook_results,'native_desktop_validation':{'Power BI':'NOT RUN','Tableau':'NOT RUN'}}
    (ROOT/'VERIFICATION.json').write_text(json.dumps(result,indent=2));print('PASS: 50 results reproduced; independent checks passed;',len(workbook_results),'Excel packages checked')
    return result
if __name__=='__main__':verify()
