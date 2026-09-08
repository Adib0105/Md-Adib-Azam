import pandas as pd
import numpy as np
import math
from pathlib import Path

DATA=Path(__file__).parents[1]/'datasets'/'marketing_campaigns.csv'
df=pd.read_csv(DATA)
roas=(df.revenue/df.spend).to_numpy(); rng=np.random.default_rng(42); means=np.array([rng.choice(roas,len(roas),replace=True).mean() for _ in range(5000)]); print({'mean_roas':roas.mean(),'bootstrap_se':means.std(),'ci_95':np.quantile(means,[.025,.975]).tolist()})
