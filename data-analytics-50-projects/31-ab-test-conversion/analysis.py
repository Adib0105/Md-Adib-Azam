import pandas as pd
import numpy as np
import math
from pathlib import Path

DATA=Path(__file__).parents[1]/'datasets'/'marketing_campaigns.csv'
df=pd.read_csv(DATA)
a=df.iloc[0]; b=df.iloc[1]; p1=a.conversions/a.clicks; p2=b.conversions/b.clicks; pooled=(a.conversions+b.conversions)/(a.clicks+b.clicks); se=np.sqrt(pooled*(1-pooled)*(1/a.clicks+1/b.clicks)); z=(p1-p2)/se; print({'lift':p1/p2-1,'z_score':z,'two_sided_p_approx':math.erfc(abs(z)/math.sqrt(2))})
