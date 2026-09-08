import pandas as pd
import numpy as np
import math
from pathlib import Path

DATA=Path(__file__).parents[1]/'datasets'/'customers.csv'
df=pd.read_csv(DATA)
cols=['age','satisfaction','monthly_spend']; print(df[cols].corr().round(3)); r=df.age.corr(df.monthly_spend); print({'age_spend_r':r,'r_squared':r*r})
