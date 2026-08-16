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

from collections import Counter


def run(output_dir=None):
    rng=np.random.default_rng(106); channels=np.array(["search","social","email","affiliate","display"]); strength=dict(search=1.0,social=.55,email=1.25,affiliate=.75,display=.3)
    paths=[]; converted=[]
    for _ in range(12000):
        path=list(rng.choice(channels,size=rng.integers(1,6),replace=True,p=[.3,.24,.18,.12,.16]))
        z=-3.1+sum(strength[c] for c in set(path))+.28*("email" in path and "search" in path)
        paths.append(path); converted.append(rng.random()<1/(1+np.exp(-z)))
    converted=np.array(converted); base=converted.mean(); effects={}
    assists=Counter()
    for c in channels:
        without=np.array([c not in p for p in paths]); counter_rate=converted[without].mean()
        effects[c]=max(0,base-counter_rate)
        assists[c]=sum(converted[i] and c in paths[i][:-1] for i in range(len(paths)))
    total=sum(effects.values()) or 1; share={c:effects[c]/total for c in channels}; top=max(share,key=share.get)
    entropy=-sum(v*np.log(v+1e-12) for v in share.values())/np.log(len(channels))
    metrics={"conversion_rate_pct":round(100*base,2),"top_incremental_channel":top,"top_attribution_share_pct":round(100*share[top],2),"attribution_diversity_index":round(float(entropy),3),"assisted_conversions":int(sum(assists.values()))}
    return save_result("marketing-attribution",metrics,[f"Protect {top} budget; it has the highest modeled removal effect.","Use assisted conversions alongside last-click reporting."],output_dir)

if __name__ == "__main__": print(json.dumps(run(),indent=2))
