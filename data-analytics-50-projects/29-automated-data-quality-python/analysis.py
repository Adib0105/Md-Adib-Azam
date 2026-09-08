import pandas as pd
import numpy as np
import json
from pathlib import Path

DATA=Path(__file__).parents[1]/'datasets'/'customers.csv'
df=pd.read_csv(DATA)
checks={'duplicate_ids':int(df.customer_id.duplicated().sum()),'missing_cells':int(df.isna().sum().sum()),'invalid_age':int((~df.age.between(18,100)).sum()),'invalid_satisfaction':int((~df.satisfaction.between(1,5)).sum())}; print(json.dumps(checks,indent=2)); assert sum(checks.values())==0
