import pandas as pd
import numpy as np
import json
from pathlib import Path

DATA=Path(__file__).parents[1]/'datasets'/'retail_sales.csv'
df=pd.read_csv(DATA)
df['revenue']=df.units*df.unit_price*(1-df.discount); med=df.revenue.median(); mad=(df.revenue-med).abs().median(); df['robust_z']=0.6745*(df.revenue-med)/mad; print(df.loc[df.robust_z.abs()>2,['order_id','revenue','robust_z']].round(2))
