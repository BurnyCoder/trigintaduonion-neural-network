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


def freeze_times(group, fits, evaluations):
    """Verify that every comparison checkpoint predates the first opened held-out result."""
    opened = [evaluations[name] for name in group if name in evaluations]
    if not all(name in fits for name in group):
        if opened:
            raise ValueError(f"{group[0]} comparison opened before all checkpoints were frozen")
        return None, None
    latest = max(datetime.fromisoformat(fits[name]["time"]) for name in group)
    if not opened:
        return latest.isoformat(), None
    first = min(datetime.fromisoformat(result["time"]) for result in opened)
    if latest > first:
        raise ValueError(f"{group[0]} comparison contains a fit after the first held-out evaluation")
    return latest.isoformat(), first.isoformat()


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
    scenes=[c.name for g in ("primary","controls") for c in runs(g)]
    images=[c.name for c in runs("images")]
    scene_fit,scene_eval=freeze_times(scenes,fits,evals)
    image_fit,image_eval=freeze_times(images,fits,evals)
    return {"planned":len(planned),"completed_training":len(fits),"completed_evaluation":len(evals),
            "checked_splits":splits,"recounted_decisions":decisions,"distinct_label_streams":len(labels),
            "full_epoch_journals_verified":len(fits),"latest_registered_scene_fit":scene_fit,
            "earliest_registered_scene_eval":scene_eval,"latest_registered_external_fit":image_fit,
            "earliest_registered_external_eval":image_eval}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true",help="also persist this verification snapshot")
    args=parser.parse_args()
    evidence=verify()
    print(json.dumps(evidence,indent=2))
    if args.write:
        write_json(RESULTS/"recount.json",evidence)
