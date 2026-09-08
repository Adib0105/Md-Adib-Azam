import pandas as pd
import numpy as np
import json
from pathlib import Path

DATA=Path(__file__).parents[1]/'datasets'/'customers.csv'
df=pd.read_csv(DATA)
risk=(df.churned*3+(df.satisfaction<=2)*2+(df.monthly_spend<df.monthly_spend.median())).astype(int)
df['risk_score']=risk
print(df.groupby('risk_score').agg(customers=('customer_id','count'),churn_rate=('churned','mean'),avg_spend=('monthly_spend','mean')).round(2))
