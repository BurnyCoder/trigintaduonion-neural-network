"""Recount raw decisions and intervene on spatial inputs of a frozen scene checkpoint."""
import csv
import gzip

import numpy as np
import torch

from .analysis import read
from .experiment import dataset,load_run
from .paths import RESULTS,write_json


def recount(directory,split,published):
    """Raw label/prediction rows are the unit-level evidence for every evaluation."""
    with gzip.open(directory/f"{split}-predictions.csv.gz","rt",encoding="utf-8") as f:
        rows=list(csv.DictReader(f))
    ids=np.array([int(r["index"]) for r in rows])
    if not np.array_equal(ids,np.arange(published["examples"])):
        raise ValueError(f"{split} has missing or repeated example indices")
    y=np.array([int(r["label"]) for r in rows])
    p=np.array([int(r["prediction"]) for r in rows])
    acc=p==y
    metrics={"accuracy":float(acc.mean())}
    if "both_correct" in published:
        if not (y[::2]+y[1::2]==1).all():
            raise ValueError(f"family label pairing failed for {split}")
        metrics.update(both_correct=float(acc.reshape(-1,2).all(1).mean()),
                       flip_fraction=float((p[::2]!=p[1::2]).mean()),
                       positive_fraction=float(y.mean()),constant_accuracy=float((y==0).mean()))
    for key,v in metrics.items():
        if abs(v-published[key])>1e-8:
            raise ValueError(f"{split} raw {key} {v} differs from released {published[key]}")
    return {"rows":len(rows),"correct":int(acc.sum()),**metrics}


@torch.inference_mode()
def interventions(model,ds,batch,device):
    """Act on visible geometry and payload correspondence without additional training."""
    outputs={k:[] for k in ("original","isometry_and_reindexing","broken_correspondence")}
    # This orthogonal reflection also rotates axes. The common translation leaves distances unchanged.
    transform=torch.tensor([[.6,.8],[.8,-.6]],device=device)
    for ids in torch.arange(len(ds),device=device).split(batch):
        f,_=ds.batch(ids)
        changed={**f,**{k:f[k]@transform+1.25 for k in ("beacon","land","pos")}}
        for k in ("beacon","land","pos","x","k","z"):
            changed[k]=changed[k].flip(1)
        # Keep the positions fixed but place the same excitation/query/reading bundles on other objects.
        broken={**f,**{k:f[k].roll(1,dims=1) for k in ("x","k","z")}}
        for key,x in zip(outputs,(f,changed,broken)):
            outputs[key].append(model(x).sigmoid().cpu())
    original=torch.cat(outputs["original"])
    y=ds.y.cpu().long()
    measures={}
    for k,parts in outputs.items():
        prob=torch.cat(parts)
        pred=prob>=.5
        measures[k]={"accuracy_against_original_labels":(pred==y).double().mean().item(),
                     "changed_decisions":int((pred!=(original>=.5)).sum()),
                     "max_probability_change":float((prob-original).abs().max()),"examples":len(y)}
    return measures


def audit(name,device="auto"):
    """Read an existing checkpoint and its completed test manifests, preserving the original evaluation."""
    cfg,model,dev=load_run(name,device)
    folder=RESULTS/name
    splits=read(folder/"eval.json")["splits"]
    result={"run":name,"recount":{split:recount(folder,split,v) for split,v in splits.items()}}
    if cfg.task=="scene":
        result["interventions"]=interventions(model,dataset(cfg,"test",dev),cfg.batch,dev)
    write_json(RESULTS/"audits"/(name+".json"),result)
    return result
