from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PORTFOLIO = Path(__file__).resolve().parents[2]
if str(PORTFOLIO) not in sys.path:
    sys.path.insert(0, str(PORTFOLIO))
from portfolio_core import save_result

from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


def run(output_dir=None):
    rng=np.random.default_rng(111); centers=np.array([[22.5726,88.3639],[22.5958,88.2636],[22.6548,88.4467],[22.4960,88.3100]])
    weights=np.array([.4,.22,.24,.14]); n=6000; c=rng.choice(len(centers),n,p=weights); coords=centers[c]+rng.normal(0,[.008,.01],(n,2)); out=rng.uniform([22.45,88.23],[22.69,88.49],(250,2)); coords=np.vstack([coords,out])
    scaled=StandardScaler().fit_transform(coords); labels=DBSCAN(eps=.16,min_samples=25).fit_predict(scaled); valid=labels>=0; unique=np.unique(labels[valid]); counts=pd.Series(labels[valid]).value_counts()
    sil=silhouette_score(scaled[valid],labels[valid]) if len(unique)>1 else 0
    metrics={"hotspots":int(len(unique)),"noise_share_pct":round(100*float((~valid).mean()),2),"silhouette_score":round(float(sil),3),"largest_hotspot_share_pct":round(100*float(counts.max()/valid.sum()),2),"covered_trips":int(valid.sum())}
    return save_result("geospatial-demand-hotspots",metrics,["Stage drivers near the two largest stable hotspots before peak windows.","Treat noise trips as coverage demand, not failed clustering."],output_dir)

if __name__ == "__main__": print(json.dumps(run(),indent=2))
