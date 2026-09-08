import pandas as pd
import numpy as np
import json
from pathlib import Path

DATA=Path(__file__).parents[1]/'datasets'/'customers.csv'
df=pd.read_csv(DATA)
df['segment']=np.select([(df.monthly_spend>=6000),(df.churned.eq(1)),(df.monthly_spend>=3000)],['High Value','At Risk','Core'],default='Emerging')
print(df.groupby('segment').agg(customers=('customer_id','count'),spend=('monthly_spend','mean'),satisfaction=('satisfaction','mean')).round(2))
