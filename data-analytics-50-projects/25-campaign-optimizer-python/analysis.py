import pandas as pd
import numpy as np
import json
from pathlib import Path

DATA=Path(__file__).parents[1]/'datasets'/'marketing_campaigns.csv'
df=pd.read_csv(DATA)
df['ctr']=df.clicks/df.impressions; df['cvr']=df.conversions/df.clicks; df['cpa']=df.spend/df.conversions; df['roas']=df.revenue/df.spend
print(df[['channel','ctr','cvr','cpa','roas']].sort_values('roas',ascending=False).round(3))
