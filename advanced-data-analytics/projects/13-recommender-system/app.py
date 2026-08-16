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
    rng=np.random.default_rng(113); users,items,k=240,150,8; u=rng.normal(size=(users,k)); v=rng.normal(size=(items,k)); truth=u@v.T+rng.normal(0,.5,(users,items)); observed=np.zeros_like(truth)
    train_mask=np.zeros_like(truth,dtype=bool); held=[]
    for i in range(users):
        liked=np.argsort(truth[i])[-18:]; hold=liked[-1]; held.append(hold); chosen=liked[:-1]; train_mask[i,chosen]=True; observed[i,chosen]=truth[i,chosen]
        noise=rng.choice(np.setdiff1d(np.arange(items),liked),8,replace=False); train_mask[i,noise]=True; observed[i,noise]=truth[i,noise]
    means=np.divide(observed.sum(1),train_mask.sum(1),where=train_mask.sum(1)>0); centered=np.where(train_mask,observed-means[:,None],0); U,s,Vt=np.linalg.svd(centered,full_matrices=False); pred=(U[:,:12]*s[:12])@Vt[:12]+means[:,None]; pred[train_mask]=-np.inf
    top=np.argsort(pred,axis=1)[:,-5:]; hits=np.array([held[i] in top[i] for i in range(users)]); coverage=len(np.unique(top))/items
    metrics={"precision_at_5":round(float(hits.mean()/5),3),"recall_at_5":round(float(hits.mean()),3),"catalog_coverage_pct":round(100*coverage,2),"users_evaluated":users,"latent_factors":12}
    return save_result("recommender-system",metrics,["A/B test ranked recommendations against popularity baseline.","Monitor coverage so personalization does not collapse to a few items."],output_dir)

if __name__ == "__main__": print(json.dumps(run(),indent=2))
