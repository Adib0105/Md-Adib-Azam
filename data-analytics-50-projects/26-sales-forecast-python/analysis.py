import pandas as pd
import numpy as np
import json
from pathlib import Path

DATA=Path(__file__).parents[1]/'datasets'/'retail_sales.csv'
df=pd.read_csv(DATA)
df['date']=pd.to_datetime(df.date); df['sales']=df.units*df.unit_price*(1-df.discount)
m=df.set_index('date').resample('MS').sales.sum(); x=np.arange(len(m)); coef=np.polyfit(x,m.values,1); forecast=np.polyval(coef,len(m)); print(m.round(2)); print('Next period forecast:',round(forecast,2))
