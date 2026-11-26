"""Release only explicitly scoped study artifacts; keep credentials and resumable local state private."""
import json
from pathlib import Path
import subprocess

from huggingface_hub import CommitOperationAdd,HfApi
from .paths import ROOT,RESULTS,CHECKPOINTS


REPO="BurnyCoder/trigintaduonion-neural-network"


def git(*args):
    proc=subprocess.run(["git",*args],cwd=ROOT,check=True,capture_output=True)
    return proc.stdout


def publish(name=""):
    """Mirror tracked research content and finished portable weights in one model collection."""
    out=RESULTS/name
    if name and Path(name).name!=name:
        raise ValueError("invalid run ID")
    scoped=["README.md","reports","docs","results","logs"]
    git("add","--",*[p for p in scoped if (ROOT/p).exists()])
    changed=bool(git("diff","--cached","--name-only"))
    if changed:
        git("commit","-m",f"Record research milestone {name or 'protocol'}")
    git("push","origin","HEAD")
    # Maintain a local acknowledgement of the last successful Hub upload.
    state=ROOT/".work"/"hub-revision.txt"
    head=git("rev-parse","HEAD").decode().strip()
    if state.exists():
        names=git("diff","--name-only","--diff-filter=ACMR","-z",state.read_text().strip(),head)
    else:
        names=git("ls-files","-z")
    ops=[]
    for raw in names.split(b"\0"):
        if not raw:
            continue
        path=raw.decode()
        if path.startswith(".github/") or path in (".gitignore",".env.example"):
            continue
        remote="research/README.md" if path=="README.md" else path
        ops.append(CommitOperationAdd(path_in_repo=remote,path_or_fileobj=ROOT/path))
    card=ROOT/"docs"/"model-card.md"
    if card.exists():
        ops.append(CommitOperationAdd(path_in_repo="README.md",path_or_fileobj=card))
    if name=="algebra":
        locations=sorted(CHECKPOINTS.glob("product-*/model.safetensors"))
    elif name:
        locations=[CHECKPOINTS/name/"model.safetensors"]
    else:
        locations=[]
    for file in locations:
        if file.exists():
            ops.append(CommitOperationAdd(path_in_repo=f"weights/{file.parent.name}/model.safetensors",
                                          path_or_fileobj=file))
    if ops:
        HfApi().create_commit(repo_id=REPO,operations=ops,commit_message=f"Study milestone {name or 'protocol'} at {head[:8]}")
    state.parent.mkdir(exist_ok=True)
    state.write_text(head)
    print(f"https://huggingface.co/{REPO}",flush=True)
