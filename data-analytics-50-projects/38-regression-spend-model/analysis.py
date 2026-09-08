import pandas as pd
import numpy as np
import math
from pathlib import Path

DATA=Path(__file__).parents[1]/'datasets'/'customers.csv'
df=pd.read_csv(DATA)
x=df.satisfaction.to_numpy(float); y=df.monthly_spend.to_numpy(float); slope=np.cov(x,y,ddof=0)[0,1]/np.var(x); intercept=y.mean()-slope*x.mean(); pred=intercept+slope*x; ssr=((y-pred)**2).sum(); r2=1-ssr/((y-y.mean())**2).sum(); print({'slope':slope,'intercept':intercept,'r_squared':r2,'rmse':np.sqrt(np.mean((y-pred)**2))})
