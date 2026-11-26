"""Natural-image benchmarks using published pixels and superpixel graphs."""
import hashlib
import io
import os
import pickle
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq
from huggingface_hub import snapshot_download
from PIL import Image
import torch
from torch import nn
from torch.nn import functional as F

from .algebra import CD32Conv2d
from .models import DistanceBlock, WIDTH
from .paths import DATA

HF_DATA = {
    "graphs": ("graphs-datasets/CIFAR10","c3d5c7aa3321c405b2818dc5f89125a84e28c7e4","data"),
    "cifar": ("uoft-cs/cifar10","0b2714987fa478483af9968de7c934580d0bb9a2","plain_text"),
}
CIFAIR_URL = "https://github.com/cvjena/cifair/releases/download/v1.0/ciFAIR-10.zip"
CIFAIR_SHA256 = "24b6bec47fb01c56fb150b501d053ea1d1f983cdb8410d4ce5bba1d25b5cff0e"


def parquet_files(source, split):
    """Use only the requested split at the pinned Hub revision."""
    repo, rev, sub = HF_DATA[source]
    root = DATA / source
    files = sorted((root/sub).glob(f"{split}-*.parquet"))
    expected = 3 if (source,split)==("graphs","train") else 1
    if len(files) != expected:
        snapshot_download(repo, repo_type="dataset", revision=rev,
                          allow_patterns=f"{sub}/{split}-*.parquet",local_dir=root)
        files = sorted((root/sub).glob(f"{split}-*.parquet"))
    if len(files) != expected:
        raise OSError(f"incomplete {source} {split} split")
    return files


def cache_npz(path, **arrays):
    """Make prepared splits atomic across interruption and process overlap."""
    from tempfile import NamedTemporaryFile
    path.parent.mkdir(parents=True,exist_ok=True)
    with NamedTemporaryFile(dir=path.parent,delete=False,suffix=".tmp") as f:
        np.savez(f,**arrays)
    os.replace(f.name,path)


class _CifarReader(pickle.Unpickler):
    """Read the specific NumPy arrays in the authors' public CIFAR-format archive."""
    def find_class(self, module, name):
        allowed = {("numpy.core.multiarray","_reconstruct"),("numpy._core.multiarray","_reconstruct"),
                   ("numpy","ndarray"),("numpy","dtype"),("_codecs","encode")}
        if (module,name) not in allowed:
            raise pickle.UnpicklingError(f"unrecognized CIFAR array type {module}.{name}")
        return super().find_class(module,name)


def pixel_arrays(split):
    """Decode original CIFAR pixels or the authors' duplicate-corrected test split."""
    key = "train" if split in ("train","val") else split
    cache = DATA / f"pixels-{key}-v1.npz"
    if not cache.exists():
        if key == "cifair":
            archive = DATA / "ciFAIR-10.zip"
            if not archive.exists():
                tmp = archive.with_suffix(".downloading")
                urllib.request.urlretrieve(CIFAIR_URL,tmp)
                os.replace(tmp,archive)
            with archive.open("rb") as f:
                if hashlib.file_digest(f,"sha256").hexdigest()!=CIFAIR_SHA256:
                    raise ValueError("ciFAIR archive digest differs from the verified release")
            with zipfile.ZipFile(archive) as z:
                file = next(n for n in z.namelist() if n.rsplit("/",1)[-1]=="test_batch")
                payload = _CifarReader(io.BytesIO(z.read(file)),encoding="bytes").load()
            payload = {k.decode() if isinstance(k,bytes) else k:v for k,v in payload.items()}
            x = np.asarray(payload["data"]).reshape(-1,3,32,32)
            y = np.asarray(payload["labels"])
        else:
            pixels, labels = [], []
            for file in parquet_files("cifar",key):
                for batch in pq.ParquetFile(file).iter_batches(batch_size=256):
                    rows = batch.to_pydict()
                    pixels.extend(np.asarray(Image.open(io.BytesIO(item["bytes"])).convert("RGB"))
                                  for item in rows["img"])
                    labels.extend(rows["label"])
            x = np.stack(pixels).transpose(0,3,1,2).copy()
            y = np.asarray(labels)
        cache_npz(cache,x=x,y=y.astype(np.int64))
    with np.load(cache,allow_pickle=False) as data:
        return data["x"],data["y"]


def split_pixels(x,y):
    """Allocate whole exact-duplicate groups to one side of a fixed stratified split."""
    groups = {}
    for i, image in enumerate(x):
        groups.setdefault(hashlib.sha256(image.tobytes()).digest(),[]).append(i)
    rng = np.random.default_rng(20261126)
    val = []
    for c in range(10):
        bucket = [members for members in groups.values() if y[members[0]]==c]
        count, target = 0, round(np.count_nonzero(y==c)*.1)
        for j in rng.permutation(len(bucket)):
            if count>=target:
                break
            val.extend(bucket[j])
            count += len(bucket[j])
    valid = np.sort(val)
    return np.setdiff1d(np.arange(len(y)),valid),valid


class PixelSet:
    """GPU-resident byte images with training-only standardization and crop/flip augmentation."""
    def __init__(self, split, device):
        x,y = pixel_arrays(split)
        stats = DATA / "pixels-split-v1.npz"
        if not stats.exists():
            tx,ty = (x,y) if split in ("train","val") else pixel_arrays("train")
            train,valid = split_pixels(tx,ty)
            training = tx[train].astype(np.float32)/255
            cache_npz(stats,train=train,val=valid,mean=training.mean((0,2,3),dtype=np.float64),
                      std=training.std((0,2,3),dtype=np.float64))
        with np.load(stats) as s:
            if split in ("train","val"):
                idx=s[split]
                x,y=x[idx],y[idx]
            self.mean=torch.tensor(s["mean"],dtype=torch.float32,device=device)[None,:,None,None]
            self.std=torch.tensor(s["std"],dtype=torch.float32,device=device)[None,:,None,None]
        self.x=torch.from_numpy(x).to(device)
        self.y=torch.from_numpy(y).to(device)
        self.training=split=="train"

    def __len__(self):
        return len(self.y)

    def batch(self, indices):
        img=self.x[indices].float().div_(255)
        if self.training:
            dev=img.device
            p=F.pad(img,(4,4,4,4),mode="reflect").permute(0,2,3,1)
            offset=torch.randint(9,(len(img),2),device=dev)
            r=torch.arange(32,device=dev)
            row=offset[:,0,None]+r
            col=offset[:,1,None]+torch.where(torch.rand((len(img),1),device=dev)<.5,31-r,r)
            img=p[torch.arange(len(img),device=dev)[:,None,None],row[:,:,None],col[:,None,:]].permute(0,3,1,2)
        return (img-self.mean)/self.std,self.y[indices]


def conv(ins,outs,k,stride,kind,seed):
    """Both real and structured networks keep the same residual block topology."""
    if kind in ("real","budget"):
        return nn.Conv2d(ins,outs,k,stride=stride,padding=k//2,bias=False)
    n=16 if kind=="cd16" else 32
    return CD32Conv2d(ins//n,outs//n,k,stride=stride,padding=k//2,bias=False,rule=kind,seed=seed)


class PixelBlock(nn.Module):
    def __init__(self,ins,outs,kind,seed):
        super().__init__()
        stride=2 if ins!=outs else 1
        self.body=nn.Sequential(conv(ins,outs,3,stride,kind,seed),nn.BatchNorm2d(outs),nn.ReLU(),
                                conv(outs,outs,3,1,kind,seed),nn.BatchNorm2d(outs))
        self.skip=(nn.Sequential(conv(ins,outs,1,stride,kind,seed),nn.BatchNorm2d(outs))
                   if stride==2 else nn.Identity())

    def forward(self,x):
        return F.relu(self.body(x)+self.skip(x))


class PixelClassifier(nn.Sequential):
    """CIFAR residual network with one learned stem, three two-convolution stages and a real head."""
    def __init__(self,kind,seed):
        widths=(6,13,26) if kind=="budget" else (32,64,128)
        a,b,c=widths
        super().__init__(nn.Conv2d(3,a,3,padding=1,bias=False),nn.BatchNorm2d(a),nn.ReLU(),
                         PixelBlock(a,a,kind,seed),PixelBlock(a,b,kind,seed),PixelBlock(b,c,kind,seed),
                         nn.AdaptiveAvgPool2d(1),nn.Flatten(),nn.Linear(c,10))


def graph_arrays(split):
    """Pack published variable-size graphs into contiguous arrays with node and edge offsets."""
    path=DATA/f"graphs-{split}-v1.npz"
    if not path.exists():
        colors,positions,edges,labels=[],[],[],[]
        for file in parquet_files("graphs",split):
            for batch in pq.ParquetFile(file).iter_batches(batch_size=64):
                for row in batch.to_pylist():
                    count=int(np.asarray(row["num_nodes"]).item())
                    feat=np.asarray(row["node_feat"],np.float32).reshape(count,-1)
                    pos=np.asarray(row["pos"],np.float32)
                    if pos.shape==(2,count):
                        pos=pos.T
                    edge=np.asarray(row["edge_index"],np.int32).reshape(2,-1).T
                    if pos.shape!=(count,2) or feat.shape[1]!=3 or edge.min()<0 or edge.max()>=count:
                        raise ValueError("unexpected published superpixel schema")
                    colors.append(feat)
                    positions.append(pos)
                    edges.append(edge.astype(np.uint16))
                    labels.append(int(np.asarray(row["y"]).item()))
        node_ptr=np.r_[0,np.cumsum([len(x) for x in colors])]
        edge_ptr=np.r_[0,np.cumsum([len(x) for x in edges])]
        cache_npz(path,x=np.concatenate(colors),pos=np.concatenate(positions),edge=np.concatenate(edges),
                  y=np.array(labels),node_ptr=node_ptr,edge_ptr=edge_ptr)
    with np.load(path) as arrays:
        return dict(arrays)


class GraphSet:
    def __init__(self,split,device):
        self.data=graph_arrays(split)
        self.device=device
        self.y=torch.tensor(self.data["y"],device=device)
        self.color_scale=255 if self.data["x"].max()>1.01 else 1
        self.pos_scale=32 if self.data["pos"].max()>2 else 1

    def __len__(self):
        return len(self.y)

    @staticmethod
    def _index(ptr,ids):
        lengths=ptr[ids+1]-ptr[ids]
        offset=np.r_[0,np.cumsum(lengths)[:-1]]
        group=np.repeat(np.arange(len(ids)),lengths)
        flat=np.arange(lengths.sum())+(ptr[ids]-offset)[group]
        return flat,group,offset

    def batch(self,indices):
        ids=indices.cpu().numpy()
        a=self.data
        ni,group,offset=self._index(a["node_ptr"],ids)
        ei,egroup,_=self._index(a["edge_ptr"],ids)
        edges=(a["edge"][ei]+offset[egroup,None]).T.copy()
        convert=lambda v: torch.from_numpy(v).to(self.device)
        f={"x":convert(a["x"][ni]/self.color_scale),"pos":convert(a["pos"][ni]/self.pos_scale),
           "edge":convert(edges),"group":convert(group),"n":len(ids)}
        return f,self.y[indices]


class SuperpixelClassifier(nn.Module):
    """Share the two spatial processor blocks; substitute color input and a graph-level mean readout."""
    def __init__(self,kind,seed):
        super().__init__()
        self.stem=nn.Linear(3,WIDTH)
        self.blocks=nn.ModuleList(DistanceBlock(kind,seed) for _ in range(2))
        self.head=nn.Sequential(nn.Linear(WIDTH,WIDTH),nn.SiLU(),nn.Linear(WIDTH,10))

    def forward(self,f):
        h=self.stem(f["x"])
        for block in self.blocks:
            h=block.sparse(h,f["pos"],f["edge"])
        pooled=h.new_zeros((f["n"],WIDTH)).index_add_(0,f["group"],h)
        denom=torch.bincount(f["group"],minlength=f["n"]).clamp_min(1)
        return self.head(pooled/denom[:,None])
