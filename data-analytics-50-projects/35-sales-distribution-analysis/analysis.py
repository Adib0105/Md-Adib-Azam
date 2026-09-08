import pandas as pd
import numpy as np
import math
from pathlib import Path

DATA=Path(__file__).parents[1]/'datasets'/'retail_sales.csv'
df=pd.read_csv(DATA)
x=(df.units*df.unit_price*(1-df.discount)).astype(float); skew=((x-x.mean())**3).mean()/x.std(ddof=0)**3; print({'mean':x.mean(),'median':x.median(),'std_dev':x.std(ddof=1),'skewness':skew})
