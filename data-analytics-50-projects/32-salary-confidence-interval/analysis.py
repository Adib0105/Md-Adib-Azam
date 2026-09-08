import pandas as pd
import numpy as np
import math
from pathlib import Path

DATA=Path(__file__).parents[1]/'datasets'/'hr_employees.csv'
df=pd.read_csv(DATA)
x=df.monthly_salary.astype(float); mean=x.mean(); se=x.std(ddof=1)/np.sqrt(len(x)); print({'mean':mean,'standard_error':se,'ci_95':(mean-1.96*se,mean+1.96*se),'n':len(x)})
