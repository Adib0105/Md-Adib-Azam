import pandas as pd
import numpy as np
import json
from pathlib import Path

DATA=Path(__file__).parents[1]/'datasets'/'retail_sales.csv'
df=pd.read_csv(DATA)
df['revenue']=df.units*df.unit_price*(1-df.discount)
print(df.groupby(['region','category']).revenue.agg(['sum','mean','count']).round(2))
print('Revenue outliers:', df.loc[(df.revenue-df.revenue.mean()).abs()>2*df.revenue.std(), ['order_id','revenue']].to_dict('records'))
