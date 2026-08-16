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

from scipy.spatial.distance import jensenshannon
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.pipeline import make_pipeline


def run(output_dir=None):
    rng=np.random.default_rng(114); pos=["excellent service","fast delivery","helpful support","great quality","easy checkout"]; neg=["late delivery","poor quality","refund delayed","app crashes","unhelpful support"]; neutral=["order arrived","standard package","used the app","contacted support","product received"]
    texts=[]; y=[]
    for i in range(3600):
        label=i%3; phrase=rng.choice([neg,neutral,pos][label]); texts.append(f"{phrase} order {rng.integers(1,700)} experience"); y.append(label)
    idx=rng.permutation(len(texts)); cut=2800; train=idx[:cut]; test=idx[cut:]; pipe=make_pipeline(TfidfVectorizer(ngram_range=(1,2),min_df=2),LogisticRegression(max_iter=700)).fit([texts[i] for i in train],np.array(y)[train]); pred=pipe.predict([texts[i] for i in test])
    old=np.array([.45,.35,.2]); new=np.array([.28,.31,.41]); drift=float(jensenshannon(old,new))
    metrics={"macro_f1":round(f1_score(np.array(y)[test],pred,average="macro"),3),"reviews_scored":len(test),"negative_share_pct":round(100*float((pred==0).mean()),2),"topic_distribution_drift":round(drift,3),"drift_alert":bool(drift>.12)}
    return save_result("nlp-sentiment-intelligence",metrics,["Route high-confidence negative reviews to service recovery.","Retrain vocabulary when the drift alert persists across two windows."],output_dir)

if __name__ == "__main__": print(json.dumps(run(),indent=2))
