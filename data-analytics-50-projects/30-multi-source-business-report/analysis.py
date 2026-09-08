import pandas as pd
import numpy as np
import json
from pathlib import Path

DATA=Path(__file__).parents[1]/'datasets'/'marketing_campaigns.csv'
df=pd.read_csv(DATA)
df['roas']=df.revenue/df.spend; df['cpa']=df.spend/df.conversions; summary=df[['spend','revenue']].sum().to_dict(); summary['portfolio_roas']=summary['revenue']/summary['spend']; summary['best_channel']=df.loc[df.roas.idxmax(),'channel']; print(json.dumps(summary,indent=2))
