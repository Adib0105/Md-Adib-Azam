"""Reproducible Superstore analyses. No network access; never modifies source data."""
from pathlib import Path
import hashlib, json, sqlite3
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent

def load():
    raw = pd.read_csv(ROOT/'datasets/source_superstore.csv', encoding='cp1252', dtype={'Postal Code':str})
    d = raw.rename(columns=lambda x:x.lower().replace(' ','_').replace('-','_'))
    for c in ['order_date','ship_date']:
        d[c] = pd.to_datetime(d[c], format='%m/%d/%Y', errors='raise')
    assert d.row_id.is_unique and len(d)==9994
    assert d.notna().all().all()
    assert d.discount.between(0,1,inclusive='left').all()
    assert (d.quantity>0).all() and (d.sales>0).all()
    d['ship_days']=(d.ship_date-d.order_date).dt.days
    assert (d.ship_days>=0).all()
    d['order_year']=d.order_date.dt.year.astype(str)
    d['order_month']=d.order_date.dt.strftime('%Y-%m')
    d['order_quarter']=d.order_date.dt.to_period('Q').astype(str)
    d['discount_band']=pd.cut(d.discount,[-.001,0,.2,.4,1],labels=['No discount','0–20%','20–40%','Above 40%']).astype(str)
    d['loss_flag']=(d.profit<0).astype(int)
    return d

def database(d):
    c=sqlite3.connect(':memory:')
    v=d.copy()
    for col in ['order_date','ship_date']:v[col]=v[col].dt.strftime('%Y-%m-%d')
    v.to_sql('superstore',c,index=False)
    c.execute('CREATE UNIQUE INDEX row_key ON superstore(row_id)')
    c.execute('CREATE INDEX orders_idx ON superstore(order_id)')
    return c

def orders(d):
    # One record per order; an order may have multiple sales lines.
    for c in ['order_date','customer_id','region','segment','ship_mode','ship_date']:
        assert d.groupby('order_id')[c].nunique().max()==1, f'Inconsistent {c} within order'
    return d.groupby('order_id',as_index=False).agg(order_date=('order_date','first'),customer_id=('customer_id','first'),region=('region','first'),segment=('segment','first'),ship_mode=('ship_mode','first'),sales=('sales','sum'),profit=('profit','sum'),quantity=('quantity','sum'),ship_days=('ship_days','max'),discount=('discount','mean'))

def python_analysis(kind,d):
    o=orders(d)
    if kind=='quality':
        return pd.DataFrame([{'check':'row_count','value':len(d)},{'check':'unique_orders','value':len(o)},{'check':'unique_customers','value':d.customer_id.nunique()},{'check':'missing_cells','value':int(d.isna().sum().sum())},{'check':'duplicate_row_ids','value':int(d.row_id.duplicated().sum())},{'check':'negative_ship_intervals','value':int((d.ship_days<0).sum())}])
    if kind=='rfm':
        ref=d.order_date.max()+pd.Timedelta(days=1)
        a=o.groupby('customer_id').agg(last_order=('order_date','max'),frequency=('order_id','count'),monetary=('sales','sum'))
        a['recency_days']=(ref-a.last_order).dt.days
        a['recency_score']=6-pd.qcut(a.recency_days.rank(method='average'),5,labels=False,duplicates='drop')-1
        a['frequency_score']=pd.qcut(a.frequency.rank(method='average'),5,labels=False,duplicates='drop')+1
        a['monetary_score']=pd.qcut(a.monetary.rank(method='average'),5,labels=False,duplicates='drop')+1
        a['rfm_sum']=a.recency_score+a.frequency_score+a.monetary_score
        return a.drop(columns='last_order').reset_index().sort_values(['rfm_sum','monetary'],ascending=False)
    if kind=='retention':
        a=o.assign(year=o.order_date.dt.year); first=a.groupby('customer_id').year.min()
        a['cohort']=a.customer_id.map(first); a['year_offset']=a.year-a.cohort
        r=a.groupby(['cohort','year_offset']).customer_id.nunique().rename('active_customers').reset_index()
        sizes=first.value_counts(); r['cohort_size']=r.cohort.map(sizes); r['retention']=r.active_customers/r.cohort_size
        return r
    if kind=='pareto':
        a=d.groupby('product_id').agg(sales=('sales','sum'),profit=('profit','sum')).sort_values('sales',ascending=False)
        a['cumulative_sales_share']=a.sales.cumsum()/a.sales.sum(); a['product_rank']=np.arange(1,len(a)+1)
        return a.reset_index()
    if kind=='forecast':
        m=d.groupby('order_month').sales.sum(); train=m.iloc[:-12]; actual=m.iloc[-12:]
        seasonal=train.iloc[-12:].to_numpy(); baseline=np.repeat(train.iloc[-3:].mean(),12)
        return pd.DataFrame({'month':actual.index,'actual_sales':actual.values,'seasonal_naive':seasonal,'three_month_mean':baseline,'seasonal_abs_error':abs(actual.values-seasonal),'mean_abs_error':abs(actual.values-baseline)})
    if kind=='anomaly':
        x=np.log1p(o.sales); median=x.median(); mad=(x-median).abs().median(); o['robust_z']=.67448975*(x-median)/mad
        o['outlier_flag']=(o.robust_z.abs()>3.5).astype(int)
        return o[['order_id','sales','profit','robust_z','outlier_flag']].sort_values('robust_z',ascending=False)
    if kind=='basket':
        from itertools import combinations
        from collections import Counter
        baskets=d.groupby('order_id').sub_category.agg(lambda x:sorted(set(x)))
        singles=Counter(v for basket in baskets for v in basket); pairs=Counter(pair for b in baskets for pair in combinations(b,2)); n=len(baskets)
        return pd.DataFrame([{'item_a':a,'item_b':b,'orders_together':cnt,'support':cnt/n,'confidence_a_to_b':cnt/singles[a],'lift':cnt*n/(singles[a]*singles[b])} for (a,b),cnt in pairs.items() if cnt>=20]).sort_values(['lift','orders_together'],ascending=False)
    if kind=='shipping':
        return o.groupby('ship_mode').agg(orders=('order_id','count'),median_days=('ship_days','median'),p90_days=('ship_days',lambda x:x.quantile(.9)),mean_days=('ship_days','mean')).reset_index()
    if kind=='repeat':
        dates=o.groupby('customer_id').order_date.agg(lambda x:sorted(set(x)))
        return pd.DataFrame([{'customer_id':cid,'unique_purchase_days':len(ds),'median_gap_days':float(np.median(np.diff(ds)/pd.Timedelta(days=1)))} for cid,ds in dates.items() if len(ds)>1]).sort_values('median_gap_days')
    if kind=='loss':
        a=d.assign(loss_amount=np.where(d.profit<0,-d.profit,0)).groupby(['state','sub_category']).agg(loss_amount=('loss_amount','sum'),net_profit=('profit','sum'),sales=('sales','sum'),loss_lines=('loss_flag','sum'))
        return a[a.loss_amount>0].reset_index().sort_values('loss_amount',ascending=False)
    raise ValueError(kind)

def statistics_analysis(kind,d):
    o=orders(d); rng=np.random.default_rng(42)
    if kind=='mean_ci':
        x=o.sales.to_numpy(); mean=x.mean(); se=stats.sem(x); low,high=stats.t.interval(.95,len(x)-1,loc=mean,scale=se)
        r=dict(n=len(x),mean_order_sales=mean,standard_error=se,lower_95=low,upper_95=high)
    elif kind=='welch':
        x=o.loc[o.region=='West','profit'].to_numpy(); y=o.loc[o.region=='Central','profit'].to_numpy(); t,p=stats.ttest_ind(x,y,equal_var=False)
        v1=x.var(ddof=1)/len(x); v2=y.var(ddof=1)/len(y); se=np.sqrt(v1+v2); df=(v1+v2)**2/(v1*v1/(len(x)-1)+v2*v2/(len(y)-1)); lo,hi=stats.t.interval(.95,df,loc=x.mean()-y.mean(),scale=se)
        r=dict(n_west=len(x),n_central=len(y),difference_profit=x.mean()-y.mean(),t=t,df=df,p_value=p,lower_95=lo,upper_95=hi)
    elif kind=='association':
        tab=pd.crosstab(o.segment,o.profit<0); chi,p,df,e=stats.chi2_contingency(tab,correction=False)
        r=dict(n=len(o),chi_square=chi,df=df,p_value=p,minimum_expected=e.min(),cramers_v=np.sqrt(chi/(len(o)*min(tab.shape[0]-1,tab.shape[1]-1))))
    elif kind=='spearman':
        rho,p=stats.spearmanr(o.discount,o.profit); r=dict(n=len(o),spearman_rho=rho,p_value=p)
    elif kind=='kruskal':
        groups=[g.ship_days.to_numpy() for _,g in o.groupby('ship_mode')]; h,p=stats.kruskal(*groups); r=dict(n=len(o),groups=len(groups),h=h,p_value=p,epsilon_squared=max(0,(h-len(groups)+1)/(len(o)-len(groups))))
    elif kind=='bootstrap':
        s=o.sales.to_numpy(); p=o.profit.to_numpy(); vals=[]
        for _ in range(2000):
            idx=rng.integers(0,len(o),len(o)); vals.append(p[idx].sum()/s[idx].sum())
        lo,hi=np.quantile(vals,[.025,.975]); r=dict(n_orders=len(o),replicates=2000,margin=p.sum()/s.sum(),lower_95=lo,upper_95=hi,bootstrap_se=np.std(vals,ddof=1))
    elif kind=='regression':
        a=o.sort_values(['order_date','order_id']); cut=int(.8*len(a)); train=a.iloc[:cut]; test=a.iloc[cut:]
        fit=stats.linregress(train.sales,train.profit); pred=fit.intercept+fit.slope*test.sales; err=test.profit-pred
        r=dict(train_orders=len(train),test_orders=len(test),slope=fit.slope,intercept=fit.intercept,train_r_squared=fit.rvalue**2,test_mae=abs(err).mean(),test_rmse=np.sqrt((err**2).mean()),test_r_squared=1-(err**2).sum()/((test.profit-test.profit.mean())**2).sum())
    elif kind=='wilson':
        n=len(o); k=int((o.profit<0).sum()); p=k/n; z=stats.norm.ppf(.975); den=1+z*z/n; center=(p+z*z/(2*n))/den; half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
        r=dict(n_orders=n,loss_orders=k,loss_rate=p,lower_95=center-half,upper_95=center+half)
    else:raise ValueError(kind)
    return pd.DataFrame([r])

def analyze(p,d,conn):
    if p.get('python'):return python_analysis(p['python'],d)
    if p.get('statistics'):return statistics_analysis(p['statistics'],d)
    return pd.read_sql_query((ROOT/p['folder']/'analysis.sql').read_text(),conn)

def fingerprint():return hashlib.sha256((ROOT/'datasets/source_superstore.csv').read_bytes()).hexdigest()
