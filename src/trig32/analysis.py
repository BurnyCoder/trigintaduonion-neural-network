"""Reconstruct registered contrasts from completed run manifests and paired world scores."""
import json
from pathlib import Path

import numpy as np

from .paths import RESULTS, LOGS


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def interval(values):
    """Student interval across independently generated worlds, in the original metric units."""
    a=np.asarray(values,dtype=float)
    if not len(a):
        return {"n":0,"mean":None,"lo":None,"hi":None}
    m=float(a.mean())
    radius=None
    if len(a)>1:
        from scipy.stats import t
        radius=float(t.ppf(.975,len(a)-1)*a.std(ddof=1)/np.sqrt(len(a)))
    return {"n":len(a),"mean":m,"lo":m-radius if radius is not None else None,
            "hi":m+radius if radius is not None else None}


def contrasts(runs):
    """Only a complete set of eight registered observations can trigger a primary decision."""
    indexed={(r["config"]["task"],r["config"]["model"],r["config"]["rule"],r["config"]["seed"]):r
             for r in runs if r["config"]["families"]==1024 and r["config"]["tag"]==""}
    def score(seed,model,rule="cd32",task="scene",split="test"):
        return indexed[task,model,rule,seed]["splits"][split]["accuracy"]
    def depth(seed):
        # Ties consistently favor the one-hop control in the prescribed ordering.
        better=max(("onehop","shallow"),key=lambda m:indexed["scene",m,"cd32",seed]["val_accuracy"])
        return score(seed,"cd32")-score(seed,better)
    specs=[
        ("Matched canonical accuracy",.60,lambda s:score(s,"cd32")),
        ("Matched randomized accuracy",.60,lambda s:score(s,"random","random")),
        ("Canonical minus randomized on canonical sensors",.01,lambda s:score(s,"cd32")-score(s,"random")),
        ("Randomized minus canonical on randomized sensors",.01,lambda s:score(s,"random","random")-score(s,"cd32","random")),
        ("Canonical minus frozen",0.,lambda s:score(s,"cd32")-score(s,"frozen")),
        ("Canonical minus validation-selected shallow control",0.,depth),
        ("Canonical minus randomized on ciFAIR-10",.01,lambda s:score(s,"cd32",task="pixel",split="cifair")-score(s,"random",task="pixel",split="cifair")),
    ]
    rows=[]
    for title,threshold,formula in specs:
        values={}
        for seed in range(8):
            try:
                values[str(seed)]=formula(seed)
            except KeyError:
                continue
        stats=interval(list(values.values()))
        decision="pending"
        if len(values)==8:
            decision=("above threshold" if stats["lo"]>threshold else
                      "below threshold" if stats["hi"]<threshold else "inconclusive")
        rows.append(dict(title=title,threshold=threshold,decision=decision,values=values,**stats))
    return rows


def collect():
    """Only read saved outputs; drawing a figure must never run inference or open a new test split."""
    runs=[]
    for path in sorted(RESULTS.glob("*/train.json")):
        record=read(path)
        test=path.with_name("eval.json")
        record["splits"]=read(test)["splits"] if test.exists() else {}
        log=LOGS/(record["name"]+".jsonl")
        epochs={}
        if log.exists():
            for line in log.read_text(encoding="utf-8").splitlines():
                event=json.loads(line)
                if event["event"]=="epoch":
                    epochs[event["epoch"]]=event
        record["curve"]=[epochs[i] for i in sorted(epochs)]
        sample=path.with_name("test-examples.json")
        if sample.exists():
            record["examples"]={k:v for k,v in read(sample).items() if k in ("beacon","land","pos","labels","predictions","scores","z","oracle")}
        runs.append(record)
    diagnostics=[row for p in sorted((RESULTS/"algebra").glob("seed-*.json")) for row in read(p)]
    return dict(runs=runs,contrasts=contrasts(runs),algebra=diagnostics)


def percent(x):
    return "pending" if x is None else f"{100*x:.2f}%"


def table(rows,headers):
    return "\n".join("| "+" | ".join(str(x) for x in row)+" |" for row in [headers,["---"]*len(headers),*rows])


def row_metrics(r):
    s=r["splits"].get("test",{})
    return [r["name"],str(r["trainable"]),percent(r["val_accuracy"]),percent(s.get("accuracy")),
            percent(s.get("both_correct")) if r["config"]["task"]=="scene" else "n/a",
            percent(r["splits"].get("heldout",{}).get("accuracy")) if r["config"]["task"]=="scene" else "n/a",
            percent((r["splits"].get("crowded",{}) if r["config"]["task"]=="scene" else r["splits"].get("cifair",{})).get("accuracy"))]


HEADERS=["Run","Trainable","Validation","Test","Both mates","Held-out channels","Crowded / ciFAIR"]
