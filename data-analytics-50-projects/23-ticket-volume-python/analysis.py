import pandas as pd
import numpy as np
import json
from pathlib import Path

DATA=Path(__file__).parents[1]/'datasets'/'support_tickets.csv'
df=pd.read_csv(DATA)
df['opened_at']=pd.to_datetime(df.opened_at)
print(df.groupby('channel').agg(tickets=('ticket_id','count'),avg_response=('first_response_min','mean'),avg_csat=('csat','mean')).round(2))
