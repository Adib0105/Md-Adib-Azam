import pandas as pd
import numpy as np
import json
from pathlib import Path

DATA=Path(__file__).parents[1]/'datasets'/'hr_employees.csv'
df=pd.read_csv(DATA)
print(df.groupby(['department','overtime']).agg(headcount=('employee_id','count'),attrition=('attrition','mean'),salary=('monthly_salary','mean'),performance=('performance','mean')).round(2))
