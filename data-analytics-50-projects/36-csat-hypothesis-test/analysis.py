import pandas as pd
import numpy as np
import math
from pathlib import Path

DATA=Path(__file__).parents[1]/'datasets'/'support_tickets.csv'
df=pd.read_csv(DATA)
x=df.csat.dropna().astype(float); target=4; t=(x.mean()-target)/(x.std(ddof=1)/np.sqrt(len(x))); d=(x.mean()-target)/x.std(ddof=1); print({'mean_csat':x.mean(),'t_statistic':t,'effect_size_d':d,'n':len(x)})
