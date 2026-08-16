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


def run(output_dir=None):
    rng=np.random.default_rng(115); n=320; groups=rng.integers(0,7,n); a=np.zeros((n,n),dtype=float)
    for i in range(n):
        p=np.where(groups==groups[i],.08,.006); links=rng.random(n)<p; links[i]=False; a[i,links]=1
    dangling=a.sum(1)==0; a[dangling,:]=1; transition=a/a.sum(1,keepdims=True); rank=np.ones(n)/n
    for _ in range(100): rank=.15/n+.85*transition.T@rank
    concentration=float(np.sort(rank)[-10:].sum()); top=np.argsort(rank)[-10:][::-1]
    # Weakly connected components without external graph packages.
    seen=set(); components=[]; undirected=(a+a.T)>0
    for start in range(n):
        if start in seen: continue
        stack=[start]; seen.add(start); comp=[]
        while stack:
            node=stack.pop(); comp.append(node)
            for nb in np.flatnonzero(undirected[node]):
                if int(nb) not in seen: seen.add(int(nb)); stack.append(int(nb))
        components.append(comp)
    metrics={"accounts":n,"edges":int(a.sum()),"communities":len(np.unique(groups)),"connected_components":len(components),"top_10_influence_share_pct":round(100*concentration,2),"top_account":int(top[0])}
    return save_result("social-network-influence",metrics,["Seed campaigns through high-rank accounts across multiple communities.","Avoid selecting influencers only by follower count; use network position."],output_dir)

if __name__ == "__main__": print(json.dumps(run(),indent=2))
