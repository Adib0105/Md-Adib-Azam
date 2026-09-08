import pandas as pd
import numpy as np
import math
from pathlib import Path

DATA=Path(__file__).parents[1]/'datasets'/'hr_employees.csv'
df=pd.read_csv(DATA)
table=pd.crosstab(df.overtime,df.attrition); expected=np.outer(table.sum(1),table.sum(0))/table.values.sum(); chi=((table.values-expected)**2/expected).sum(); dof=(table.shape[0]-1)*(table.shape[1]-1); v=np.sqrt(chi/table.values.sum()); print(table); print({'chi_square':chi,'dof':dof,'cramers_v':v})
