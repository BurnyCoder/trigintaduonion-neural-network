"""Check analysis gating, natural adapters, data isolation and real checkpoint round trips."""
from dataclasses import replace
import numpy as np
import torch

from trig32.analysis import contrasts
from trig32.vision import PixelClassifier,SuperpixelClassifier,split_pixels


def test_decisions_require_eight_matched_worlds():
    rows=[]
    for seed in range(8):
        for model in ("cd32","random"):
            for rule in ("cd32","random"):
                rows.append(dict(config=dict(task="scene",model=model,rule=rule,seed=seed,families=1024,tag=""),
                                 splits={"test":{"accuracy":.82 if model==rule else .53}},val_accuracy=.7))
    assert contrasts(rows[:-1])[3]["decision"]=="pending"
    assert all(c["decision"]=="above threshold" for c in contrasts(rows)[:4])


def test_duplicate_isolation_and_natural_adapters():
    x=np.arange(100,dtype=np.uint8).reshape(100,1)
    x[1]=x[0]
    train,val=split_pixels(x,np.arange(100)//10)
    assert not set(x[train].ravel()).intersection(x[val].ravel())
    img=torch.randn(2,3,32,32)
    for rule in ("cd32","random","real","cd16","budget"):
        out=PixelClassifier(rule,1)(img)
        assert out.shape==(2,10)
        out.mean().backward()
    graph={"x":torch.randn(6,3),"pos":torch.rand(6,2),"edge":torch.tensor([[0,1,1,2,3,4,4,5],[1,0,2,1,4,3,5,4]]),
           "group":torch.tensor([0,0,0,1,1,1]),"n":2}
    logits=SuperpixelClassifier("cd32",0)(graph)
    assert logits.shape==(2,10) and logits.isfinite().all()
    logits.square().mean().backward()


def test_stopped_training_reloads_portable_best(tmp_path,monkeypatch):
    from trig32 import experiment as ex,paths
    from safetensors.torch import load_file
    for module in (paths,ex):
        for key in ("RESULTS","LOGS","CHECKPOINTS"):
            monkeypatch.setattr(module,key,tmp_path/key)
    cfg=ex.Config(families=12,epochs=2,batch=24,seed=31,tag="interrupted")
    assert ex.train(cfg,"cpu",stop_after=1)["epoch"]==1
    completed=ex.train(cfg,"cpu")
    full=replace(cfg,tag="uninterrupted")
    ex.train(full,"cpu")
    saved=load_file(str(ex.CHECKPOINTS/cfg.name/"model.safetensors"))
    reference=load_file(str(ex.CHECKPOINTS/full.name/"model.safetensors"))
    for name in saved:
        torch.testing.assert_close(saved[name],reference[name],atol=0,rtol=0)
    _,model,device=ex.load_run(cfg.name,"cpu")
    obs,labels=ex.dataset(cfg,"val",device).batch(torch.arange(4))
    assert model(obs).shape==labels.shape and completed["best_epoch"] in (1,2)
