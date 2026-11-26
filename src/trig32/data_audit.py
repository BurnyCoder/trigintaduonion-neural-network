"""Verify benchmark source shapes, class counts, pixel-group splits and training-only scaling."""
import gc
import hashlib

import numpy as np

from .paths import DATA,RESULTS,write_json,log_event
from .vision import HF_DATA,CIFAIR_SHA256,pixel_arrays,PixelSet,graph_arrays


def fingerprints(x):
    """Use byte equality on the decoded channel-first uint8 tensors for exact-duplicate checks."""
    return [hashlib.sha256(image.tobytes()).digest() for image in x]


def data_audit():
    # PixelSet constructs its split and normalization from original training pixels only.
    val=PixelSet("val","cpu")
    del val
    train,y=pixel_arrays("train")
    hashes=fingerprints(train)
    del train
    with np.load(DATA/"pixels-split-v1.npz") as split:
        a,b=split["train"],split["val"]
        training={hashes[i] for i in a}
        validation={hashes[i] for i in b}
        overlap=len(training&validation)
        if overlap or np.intersect1d(a,b).size or len(a)+len(b)!=len(y):
            raise ValueError("invalid or contaminated image validation split")
        pixels={"train":len(a),"validation":len(b),"training_class_counts":np.bincount(y[a]).tolist(),
                "validation_class_counts":np.bincount(y[b]).tolist(),"exact_train_val_overlap":overlap,
                "rgb_mean":split["mean"].tolist(),"rgb_std":split["std"].tolist()}
    for key in ("test","cifair"):
        x,y=pixel_arrays(key)
        digest=fingerprints(x)
        pixels[key]={"count":len(y),"class_counts":np.bincount(y).tolist(),
                     "images_seen_exactly_in_training":sum(h in training for h in digest)}
        del x
    log_event("data",event="pixels_verified",**pixels)
    graphs={}
    for split in ("train","val","test"):
        data=graph_arrays(split)
        stats={"graphs":len(data["y"]),"nodes":len(data["x"]),"edges":len(data["edge"]),
               "class_counts":np.bincount(data["y"]).tolist(),
               "color_range":[float(data["x"].min()),float(data["x"].max())],
               "position_range":[float(data["pos"].min()),float(data["pos"].max())]}
        if data["node_ptr"][-1]!=stats["nodes"] or data["edge_ptr"][-1]!=stats["edges"]:
            raise ValueError(f"unmatched graph pointers in {split}")
        graphs[split]=stats
        if split=="test":
            # Compare node colors to the original images in both coordinate conventions.
            images,labels=pixel_arrays("test")
            count=min(128,len(labels))
            ptr=data["node_ptr"][:count+1]
            row,col=np.rint(data["pos"][:ptr[-1]]*32).astype(int).clip(0,31).T
            group=np.repeat(np.arange(count),np.diff(ptr))
            rgb=images[:count].transpose(0,2,3,1)/255
            observed=data["x"][:ptr[-1]]
            stats["pixel_alignment"]={"images":count,"matching_labels":int((labels==data["y"]).sum()),
                                      "row_column_mse":float(np.square(rgb[group,row,col]-observed).mean()),
                                      "column_row_mse":float(np.square(rgb[group,col,row]-observed).mean())}
        log_event("data",event="graph_split_verified",split=split,**stats)
        del data
        gc.collect()
    result={"revisions":{k:v[1] for k,v in HF_DATA.items()},"cifair_sha256":CIFAIR_SHA256,
            "pixels":pixels,"graphs":graphs}
    write_json(RESULTS/"data-audit.json",result)
    return result
