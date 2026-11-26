"""Restartable staged study. Every actual model runs through the public training functions."""
import json
import subprocess
import sys
import time
from pathlib import Path

from .paths import RESULTS,ROOT,log_event,write_json
from .protocol import STAGES,runs


def command(*args):
    subprocess.run([sys.executable,"-m","trig32.cli",*map(str,args)],cwd=ROOT,check=True)


def milestone(name,phase,public):
    marker=ROOT/".work"/"releases"/(name+"-"+phase+("-public" if public else "-local")+".json")
    if marker.is_file():
        return
    command("report")
    if public:
        # A retry only republishes persisted artifacts; it never restarts a completed fit.
        for attempt in range(4):
            try:
                command("publish","--run",name)
                break
            except subprocess.CalledProcessError:
                if attempt==3:
                    raise
                time.sleep(10*(attempt+1))
    write_json(marker,{"name":name,"phase":phase})


def matrix(stage,public):
    stages=STAGES if stage=="all" else [stage]
    queued=[]
    for group in stages:
        configs=runs(group)
        for cfg in configs:
            if not (RESULTS/cfg.name/"train.json").exists():
                command("train","--task",cfg.task,"--model",cfg.model,"--rule",cfg.rule,"--seed",cfg.seed,
                        "--epochs",cfg.epochs,"--lr",cfg.lr,"--families",cfg.families,"--batch",cfg.batch)
            milestone(cfg.name,"fit",public)
        queued.extend(configs)
        # When orchestrating the full study, lock the depth controls before opening primary outcomes.
        if group=="primary":
            continue
        if group=="controls" and stage=="controls":
            primary=runs("primary")
            if not all((RESULTS/c.name/"train.json").exists() for c in primary):
                raise RuntimeError("finish the registered primary fits before opening confirmatory tests")
            queued=primary+queued
        for cfg in queued:
            if not (RESULTS/cfg.name/"eval.json").exists():
                command("evaluate",cfg.name)
            milestone(cfg.name,"eval",public)
        queued.clear()
        if group=="pilot":
            for seed in range(8):
                if not (RESULTS/"algebra"/f"seed-{seed}.json").exists():
                    command("algebra","--seeds",seed)
                milestone("algebra",f"seed-{seed}",public)
        log_event("study",event="stage_complete",stage=group)

