"""Common entry points for training, checkpoint recovery, evaluation and exported inference."""
from dataclasses import asdict, dataclass
import gzip
import json
import os
import platform
import subprocess
import time
from pathlib import Path

import numpy as np
from filelock import FileLock
from safetensors.torch import load_file, save_file
import torch
from torch.nn import functional as F
from torch.utils.tensorboard import SummaryWriter

from .models import SceneClassifier
from .paths import CHECKPOINTS, LOGS, RESULTS, ROOT, log_event, now, write_json
from .scenes import SceneSet
from .vision import GraphSet, PixelClassifier, PixelSet, SuperpixelClassifier


@dataclass(frozen=True)
class Config:
    task: str = "scene"
    model: str = "cd32"
    rule: str = "cd32"
    seed: int = 42
    families: int = 1024
    epochs: int = 80
    batch: int = 128
    lr: float = .003
    tag: str = ""

    @property
    def name(self):
        parts=[self.task,self.model,self.rule,f"s{self.seed}"]
        if self.task=="scene":
            parts.append(f"n{self.families}")
        if self.tag:
            if not self.tag.replace("-","").isalnum():
                raise ValueError("use alphanumeric run tags")
            parts.append(self.tag)
        return "-".join(parts)


def hardware(device):
    """Record the hardware and source revision used for each experiment."""
    git=subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,capture_output=True,text=True)
    return {"device":str(device),"gpu":torch.cuda.get_device_name(device) if device.type=="cuda" else None,
            "torch":str(torch.__version__),"cuda":torch.version.cuda,"python":platform.python_version(),
            "commit":git.stdout.strip() or None}


def setup(device,seed):
    torch.set_num_threads(min(4,os.cpu_count() or 1))
    torch.manual_seed(seed)
    np.random.seed(seed)
    torch.set_float32_matmul_precision("high")
    return torch.device("cuda" if torch.cuda.is_available() else "cpu") if device=="auto" else torch.device(device)


def build(cfg):
    """Construct only from the public task, model and seed configuration."""
    if cfg.task=="scene":
        return SceneClassifier(cfg.model,cfg.seed)
    if cfg.task=="pixel":
        return PixelClassifier(cfg.model,cfg.seed)
    if cfg.task=="graph":
        return SuperpixelClassifier(cfg.model,cfg.seed)
    raise ValueError(f"unknown task {cfg.task}")


def dataset(cfg,split,device):
    if cfg.task=="scene":
        families=cfg.families if split=="train" else 256 if split=="val" else 1024
        return SceneSet(families,cfg.seed,split,cfg.rule,device)
    if cfg.task=="pixel":
        return PixelSet(split,device)
    return GraphSet(split,device)


def loss_predictions(logits,y):
    if logits.ndim==1:
        return F.binary_cross_entropy_with_logits(logits,y), (logits>=0).long()
    return F.cross_entropy(logits,y), logits.argmax(-1)


@torch.inference_mode()
def measure(model,ds,batch,device):
    """Return metrics and individually reconstructible predictions, including mate outcomes."""
    model.eval()
    losses,preds,labels,conf=[],[],[],[]
    for idx in torch.arange(len(ds),device=device).split(batch):
        x,y=ds.batch(idx)
        logits=model(x)
        loss,p=loss_predictions(logits,y)
        prob=logits.sigmoid() if logits.ndim==1 else logits.softmax(-1).amax(-1)
        losses.append(loss*len(y))
        preds.append(p)
        labels.append(y.long())
        conf.append(prob)
    preds,labels,conf=[torch.cat(items).cpu().numpy() for items in (preds,labels,conf)]
    correct=preds==labels
    metrics={"accuracy":float(correct.mean()),"loss":float(torch.stack(losses).sum().item()/len(ds)),
             "examples":len(ds)}
    if isinstance(ds,SceneSet):
        metrics.update(both_correct=float(correct.reshape(-1,2).all(1).mean()),
                       flip_fraction=float((preds[::2]!=preds[1::2]).mean()),
                       positive_fraction=float(labels.mean()))
    return metrics,{"prediction":preds,"label":labels,"score":conf}


def train(cfg,device="auto",stop_after=None):
    """Resume completed epochs exactly using an epoch-keyed sampler, RNG and optimizer state."""
    device=setup(device,cfg.seed)
    cp=CHECKPOINTS/cfg.name
    cp.mkdir(parents=True,exist_ok=True)
    with FileLock(str(cp/"run.lock"),timeout=0):
        return _train_locked(cfg,device,cp,stop_after)


def _train_locked(cfg,device,cp,stop_after):
    out=RESULTS/cfg.name
    out.mkdir(parents=True,exist_ok=True)
    complete=out/"train.json"
    if complete.exists():
        existing=json.loads(complete.read_text())
        if existing["config"]!=asdict(cfg):
            raise ValueError("run name already has a different configuration")
        return existing
    model=build(cfg).to(device)
    trainset,valset=dataset(cfg,"train",device),dataset(cfg,"val",device)
    params=[p for p in model.parameters() if p.requires_grad]
    optimizer=(torch.optim.SGD(params,lr=cfg.lr,momentum=.9,weight_decay=.0005)
               if cfg.task=="pixel" else torch.optim.AdamW(params,lr=cfg.lr,weight_decay=.0001))
    scheduler=torch.optim.lr_scheduler.CosineAnnealingLR(optimizer,T_max=cfg.epochs)
    last=cp/"last.pt"
    epoch0,best,best_epoch,seconds=0,-1.,0,0.
    if last.exists():
        state=torch.load(last,map_location=device,weights_only=True)
        if state["config"]!=asdict(cfg):
            raise ValueError("checkpoint configuration mismatch")
        model.load_state_dict(state["model"])
        optimizer.load_state_dict(state["optimizer"])
        scheduler.load_state_dict(state["scheduler"])
        epoch0,best,best_epoch,seconds=(state[k] for k in ("epoch","best","best_epoch","seconds"))
    meta=hardware(device)
    trainable=sum(p.numel() for p in params)
    total=sum(p.numel() for p in model.parameters())
    writer=SummaryWriter(str(LOGS/"tensorboard"/cfg.name),purge_step=epoch0+1)
    log_event(cfg.name,event="start",epoch=epoch0,trainable=trainable,**meta)
    if device.type=="cuda":
        torch.cuda.reset_peak_memory_stats(device)
    try:
        for epoch in range(epoch0+1,cfg.epochs+1):
            t=time.perf_counter()
            torch.manual_seed(cfg.seed*100003+epoch)
            model.train()
            order=torch.randperm(len(trainset),device=device)
            accum=torch.zeros(2,device=device)
            for ids in order.split(cfg.batch):
                f,y=trainset.batch(ids)
                optimizer.zero_grad(set_to_none=True)
                logits=model(f)
                loss,pred=loss_predictions(logits,y)
                loss.backward()
                optimizer.step()
                accum+=torch.stack((loss.detach()*len(y),(pred==y).sum()))
            scheduler.step()
            stats,_=measure(model,valset,cfg.batch,device)
            sums=accum.cpu().tolist()
            if not np.isfinite(sums[0]+stats["loss"]):
                raise FloatingPointError(f"non-finite objective at epoch {epoch}")
            if stats["accuracy"]>best:
                best,best_epoch=stats["accuracy"],epoch
                # Save separate candidates before atomically advancing the epoch checkpoint.
                save_file({k:v.detach().contiguous().cpu() for k,v in model.state_dict().items()},
                          str(cp/f"best-{epoch}.tmp"))
                os.replace(cp/f"best-{epoch}.tmp",cp/f"best-{epoch}.safetensors")
            elapsed=time.perf_counter()-t
            seconds+=elapsed
            state={"model":model.state_dict(),"optimizer":optimizer.state_dict(),"scheduler":scheduler.state_dict(),
                   "config":asdict(cfg),"epoch":epoch,"best":best,"best_epoch":best_epoch,"seconds":seconds}
            torch.save(state,cp/"last.tmp")
            os.replace(cp/"last.tmp",last)
            record=log_event(cfg.name,event="epoch",epoch=epoch,epochs=cfg.epochs,
                             train_loss=sums[0]/len(trainset),train_accuracy=sums[1]/len(trainset),
                             val_loss=stats["loss"],val_accuracy=stats["accuracy"],epoch_seconds=elapsed)
            write_json(out/"live.json",record)
            for k in ("train_loss","train_accuracy","val_loss","val_accuracy"):
                writer.add_scalar(k,record[k],epoch)
            writer.flush()
            if stop_after is not None and epoch>=stop_after and epoch<cfg.epochs:
                return record
        import shutil
        shutil.copyfile(cp/f"best-{best_epoch}.safetensors",cp/"model.tmp")
        os.replace(cp/"model.tmp",cp/"model.safetensors")
        result={"config":asdict(cfg),"name":cfg.name,"time":now(),"hardware":meta,"trainable":trainable,
                "parameters":total,"best_epoch":best_epoch,"val_accuracy":best,
                "train_examples":len(trainset),"val_examples":len(valset),"seconds":seconds,
                "training_examples_per_second":len(trainset)*cfg.epochs/max(seconds,1e-9),
                "peak_gpu_bytes":torch.cuda.max_memory_allocated(device) if device.type=="cuda" else 0}
        if cfg.task=="pixel":
            result["normalization"]={k:getattr(trainset,k).flatten().tolist() for k in ("mean","std")}
        write_json(complete,result)
        log_event(cfg.name,event="trained",val_accuracy=best,best_epoch=best_epoch)
        return result
    finally:
        writer.close()


def load_run(name,device="auto",weights=None):
    if Path(name).name!=name:
        raise ValueError("run name must be a single path component")
    d=json.loads((RESULTS/name/"train.json").read_text())
    cfg=Config(**d["config"])
    dev=setup(device,cfg.seed)
    model=build(cfg).to(dev)
    file=Path(weights) if weights else CHECKPOINTS/name/"model.safetensors"
    if not weights and not file.exists():
        from huggingface_hub import hf_hub_download
        from .release import REPO
        file=Path(hf_hub_download(REPO,f"weights/{name}/model.safetensors"))
    model.load_state_dict(load_file(str(file),device="cpu"))
    return cfg,model.eval(),dev


def evaluate(name,device="auto"):
    """Test a fixed checkpoint on each prespecified split, retaining all per-example outcomes."""
    cfg,model,dev=load_run(name,device)
    splits=("test","heldout","crowded") if cfg.task=="scene" else ("test","cifair") if cfg.task=="pixel" else ("test",)
    result={}
    out=RESULTS/name
    for split in splits:
        ds=dataset(cfg,split,dev)
        metrics,rows=measure(model,ds,cfg.batch,dev)
        if cfg.task=="scene":
            oracle=ds.oracle(ds.features)
            metrics["oracle_accuracy"]=float((oracle==ds.y).float().mean().item())
            metrics["constant_accuracy"]=float((ds.y==0).float().mean().item())
            example={k:v[:6].cpu().tolist() for k,v in ds.features.items() if k!="x"}
            example.update(x=ds.features["x"][:6].cpu().tolist(),labels=rows["label"][:6].tolist(),
                           scores=rows["score"][:6].tolist(),predictions=rows["prediction"][:6].tolist(),
                           oracle=oracle[:6].long().cpu().tolist())
            write_json(out/f"{split}-examples.json",example)
        with gzip.open(out/f"{split}-predictions.csv.gz.tmp","wt",encoding="utf-8",newline="") as f:
            f.write("index,label,prediction,score\n")
            for i,(y,p,s) in enumerate(zip(rows["label"],rows["prediction"],rows["score"])):
                f.write(f"{i},{y},{p},{s:.8g}\n")
        os.replace(out/f"{split}-predictions.csv.gz.tmp",out/f"{split}-predictions.csv.gz")
        result[split]=metrics
        log_event(name,event="evaluated",split=split,**metrics)
    write_json(out/"eval.json",{"time":now(),"splits":result})
    return result
