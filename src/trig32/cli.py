"""User entry points. All training and prediction use the same public model constructors."""
import argparse
import json
from pathlib import Path


def main():
    parser=argparse.ArgumentParser(prog="trig32")
    sub=parser.add_subparsers(dest="cmd",required=True)
    t=sub.add_parser("train")
    t.add_argument("--task",choices=["scene","pixel","graph"],default="scene")
    t.add_argument("--model",default="cd32")
    t.add_argument("--rule",choices=["cd32","random"],default="cd32")
    t.add_argument("--seed",type=int,default=42)
    t.add_argument("--families",type=int,default=1024)
    t.add_argument("--epochs",type=int)
    t.add_argument("--batch",type=int,default=128)
    t.add_argument("--lr",type=float)
    t.add_argument("--tag",default="")
    t.add_argument("--device",default="auto")
    e=sub.add_parser("evaluate")
    e.add_argument("run")
    e.add_argument("--device",default="auto")
    audit_parser=sub.add_parser("audit",help="verify saved predictions and probe a frozen checkpoint")
    audit_parser.add_argument("run")
    audit_parser.add_argument("--device",default="auto")
    p=sub.add_parser("predict")
    p.add_argument("run")
    p.add_argument("--input",type=Path,help="scene JSON or RGB image")
    p.add_argument("--weights",type=Path)
    p.add_argument("--index",type=int,default=0)
    p.add_argument("--device",default="auto")
    a=sub.add_parser("algebra")
    a.add_argument("--seeds",type=int,nargs="+",default=[0])
    sub.add_parser("report")
    sub.add_parser("data-audit",help="verify the published natural-image inputs and split isolation")
    sub.add_parser("dashboard").add_argument("--port",type=int,default=18332)
    m=sub.add_parser("matrix")
    m.add_argument("--stage",choices=["pilot","primary","controls","sensitivity","images","all"],default="all")
    m.add_argument("--publish",action="store_true")
    sub.add_parser("publish").add_argument("--run",default="")
    args=parser.parse_args()
    if args.cmd=="train":
        from .experiment import Config,train
        cfg=Config(args.task,args.model,args.rule,args.seed,args.families,
                   args.epochs or (80 if args.task=="scene" else 60),args.batch,
                   args.lr or (.1 if args.task=="pixel" else .003),args.tag)
        print(json.dumps(train(cfg,args.device)))
    elif args.cmd=="evaluate":
        from .experiment import evaluate
        print(json.dumps(evaluate(args.run,args.device)))
    elif args.cmd=="data-audit":
        from .data_audit import data_audit
        print(json.dumps(data_audit()))
    elif args.cmd=="audit":
        from .audit import audit
        print(json.dumps(audit(args.run,args.device)))
    elif args.cmd=="predict":
        predict(args)
    elif args.cmd=="algebra":
        from .diagnostics import diagnostics
        print(json.dumps(diagnostics(args.seeds)))
    elif args.cmd=="report":
        from .report import report
        report()
    elif args.cmd=="publish":
        from .release import publish
        publish(args.run)
    elif args.cmd=="dashboard":
        from .dashboard import serve
        serve(args.port)
    else:
        from .matrix import matrix
        matrix(args.stage,args.publish)


def predict(args):
    """Read an external scene or image, or reproduce a deterministic held-out example."""
    import torch
    import numpy as np
    from PIL import Image
    from .experiment import load_run,dataset
    from .paths import RESULTS
    cfg,model,dev=load_run(args.run,args.device,args.weights)
    if args.input and cfg.task=="scene":
        data=json.loads(args.input.read_text(encoding="utf-8"))
        # Accept the published batched example format and a user's single unbatched scene.
        f={k:torch.as_tensor(data[k],dtype=torch.long if k=="k" else torch.float32,device=dev)
           for k in ("beacon","land","pos","x","k","z")}
        if f["beacon"].ndim==2:
            f={k:v.unsqueeze(0) for k,v in f.items()}
        else:
            f={k:v[[args.index]] for k,v in f.items()}
    elif args.input and cfg.task=="pixel":
        stats=json.loads((RESULTS/args.run/"train.json").read_text())["normalization"]
        image=np.asarray(Image.open(args.input).convert("RGB").resize((32,32)),np.float32)/255
        values=(image-np.asarray(stats["mean"]))/np.asarray(stats["std"])
        f=torch.as_tensor(values.transpose(2,0,1),device=dev,dtype=torch.float32)[None]
    elif args.input:
        graph=json.loads(args.input.read_text(encoding="utf-8"))
        f={k:torch.as_tensor(graph[k],dtype=torch.long if k=="edge" else torch.float32,device=dev)
           for k in ("x","pos","edge")}
        if f["x"].ndim!=2 or f["x"].shape[1]!=3 or f["pos"].shape!=(len(f["x"]),2) or f["edge"].ndim!=2 or f["edge"].shape[0]!=2:
            raise ValueError("expected x[N,3], pos[N,2] and edge[2,E]")
        if not len(f["x"]) or (f["edge"].numel() and (f["edge"].min()<0 or f["edge"].max()>=len(f["x"]))):
            raise ValueError("graph must contain nodes and valid zero-based edge indices")
        f.update(n=1,group=torch.zeros(len(f["x"]),dtype=torch.long,device=dev))
    else:
        ds=dataset(cfg,"test",dev)
        f,_=ds.batch(torch.tensor([args.index],device=dev))
    with torch.inference_mode():
        out=model(f)
        prob=out.sigmoid() if cfg.task=="scene" else out.softmax(-1)
        pred=(prob>=.5).int() if cfg.task=="scene" else prob.argmax(-1)
    print(json.dumps({"run":args.run,"prediction":pred.item(),"probabilities":prob.cpu().tolist()}))


if __name__=="__main__":
    main()
