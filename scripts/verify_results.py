"""Verify released numbers directly from individual rows and epoch journals, without inference."""
import argparse
import csv
from datetime import datetime
import gzip
import hashlib
import json

import numpy as np
from trig32.paths import LOGS,RESULTS,write_json
from trig32.protocol import STAGES,runs


def verify():
    planned={c.name:c for stage in STAGES for c in runs(stage)}
    fits,evals,labels={},{},{}
    splits=decisions=0
    for name,c in planned.items():
        folder=RESULTS/name
        if not (folder/"train.json").exists():
            continue
        fit=json.loads((folder/"train.json").read_text(encoding="utf-8"))
        fits[name]=fit
        epochs={}
        for line in (LOGS/(name+".jsonl")).read_text(encoding="utf-8").splitlines():
            e=json.loads(line)
            if e["event"]=="epoch":
                epochs[e["epoch"]]=e
        if set(epochs)!=set(range(1,c.epochs+1)):
            raise ValueError(f"{name} has an incomplete epoch journal")
        best=max(sorted(epochs),key=lambda i:epochs[i]["val_accuracy"])
        if best!=fit["best_epoch"] or epochs[best]["val_accuracy"]!=fit["val_accuracy"]:
            raise ValueError(f"{name} checkpoint selection disagrees with validation history")
        if not (folder/"eval.json").exists():
            continue
        result=json.loads((folder/"eval.json").read_text(encoding="utf-8"))
        evals[name]=result
        for split,metrics in result["splits"].items():
            with gzip.open(folder/f"{split}-predictions.csv.gz","rt",encoding="utf-8") as f:
                rows=list(csv.DictReader(f))
            ids=np.array([int(r["index"]) for r in rows])
            y=np.array([int(r["label"]) for r in rows],np.int8)
            p=np.array([int(r["prediction"]) for r in rows],np.int8)
            correct=y==p
            if not np.array_equal(ids,np.arange(metrics["examples"])) or abs(correct.mean()-metrics["accuracy"])>1e-8:
                raise ValueError(f"{name}/{split} prediction count or accuracy mismatch")
            if c.task=="scene":
                if not (y[::2]+y[1::2]==1).all():
                    raise ValueError(f"{name}/{split} lost opposite-label mates")
                if abs(correct.reshape(-1,2).all(1).mean()-metrics["both_correct"])>1e-8:
                    raise ValueError(f"{name}/{split} paired accuracy mismatch")
                if abs((p[::2]!=p[1::2]).mean()-metrics["flip_fraction"])>1e-8:
                    raise ValueError(f"{name}/{split} decision reversal mismatch")
            key=(c.seed,split) if c.task=="scene" else (c.task,split)
            digest=hashlib.sha256(y.tobytes()).hexdigest()
            if labels.setdefault(key,digest)!=digest:
                raise ValueError(f"{name}/{split} different labels in a paired comparison")
            splits+=1
            decisions+=len(y)
    group=[c.name for g in ("primary","controls") for c in runs(g)]
    opened=[evals[n] for n in group if n in evals]
    last_fit=first_eval=None
    if opened:
        if not all(n in fits for n in group):
            raise ValueError("the confirmatory analysis opened before its checkpoints were frozen")
        last_fit=max(datetime.fromisoformat(fits[n]["time"]) for n in group)
        first_eval=min(datetime.fromisoformat(e["time"]) for e in opened)
        if last_fit>first_eval:
            raise ValueError("the confirmatory evaluation chronology failed")
    return {"planned":len(planned),"completed_training":len(fits),"completed_evaluation":len(evals),
            "checked_splits":splits,"recounted_decisions":decisions,"distinct_label_streams":len(labels),
            "full_epoch_journals_verified":len(fits),"latest_registered_scene_fit":last_fit.isoformat() if last_fit else None,
            "earliest_registered_scene_eval":first_eval.isoformat() if first_eval else None}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true",help="also persist this verification snapshot")
    args=parser.parse_args()
    evidence=verify()
    print(json.dumps(evidence,indent=2))
    if args.write:
        write_json(RESULTS/"recount.json",evidence)
