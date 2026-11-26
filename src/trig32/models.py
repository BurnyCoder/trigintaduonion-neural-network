"""End-to-end geometric scene models, with identical geometry in the crossed conditions."""
import torch
from torch import nn
from torch.nn import functional as F

from .algebra import CD32Linear

KINDS = ("cd32","random","cd16","real","budget","frozen","onehop","shallow")
WIDTH = 32


class ChannelMap(nn.Module):
    """Adapt grouped hypercomplex kernels or ordinary real maps to flat feature channels."""
    def __init__(self, ins, outs, kind, seed):
        super().__init__()
        self.n = 16 if kind == "cd16" else 32
        self.structured = kind in ("cd32","random","cd16")
        if self.structured:
            self.operation = CD32Linear(ins//self.n, outs//self.n, rule=kind, seed=seed, bias=False)
        elif kind == "budget":
            # Low-rank real maps decouple channel-sharing structure from the trainable budget.
            rank = max(1, round(ins*outs/(32*(ins+outs))))
            self.operation = nn.Sequential(nn.Linear(ins,rank,bias=False), nn.Linear(rank,outs,bias=False))
        else:
            self.operation = nn.Linear(ins,outs,bias=False)

    def forward(self, x):
        if self.structured:
            return self.operation(x.unflatten(-1,(-1,self.n))).flatten(-2)
        return self.operation(x)


class Sensor(nn.Module):
    """Compare noisy coordinate observations against learned projections of the excitation."""
    def __init__(self, kind, seed, banks=4):
        super().__init__()
        self.banks = banks
        self.mix = ChannelMap(32,32*banks,kind,seed)
        self.encode = nn.Sequential(nn.Linear(2*banks+1,WIDTH), nn.SiLU(), nn.Linear(WIDTH,WIDTH))
        # Learned tied projections begin at the scale of unit-variance sensor responses.
        self.gain = nn.Parameter(torch.ones(banks))

    def forward(self, x, k, z):
        projections = self.mix(x).unflatten(-1,(self.banks,32))
        select = k[...,None,None].expand(*k.shape,self.banks,1)
        measured = projections.gather(-1,select).squeeze(-1)
        paired = measured * z[...,None] * self.gain
        return self.encode(torch.cat((measured,paired,z[...,None]),dim=-1))


class DistanceBlock(nn.Module):
    """Learn invariant scalar attention and residual feature updates over candidate neighbors.

    Fixed-position specialization of distance-conditioned messages:
    https://proceedings.mlr.press/v139/satorras21a.html .
    """
    def __init__(self, kind, seed):
        super().__init__()
        self.value = ChannelMap(WIDTH,WIDTH,kind,seed)
        self.update = ChannelMap(WIDTH,WIDTH,kind,seed)
        self.gate = nn.Sequential(nn.Linear(1,8),nn.SiLU(),nn.Linear(8,1))
        self.log_precision = nn.Parameter(torch.tensor(4.5))

    def transform(self, h):
        return h + self.value(h)

    def scores(self, d2):
        return self.gate(d2[...,None]).squeeze(-1) - self.log_precision.clamp(0,8).exp()*d2

    def finish(self, agg):
        return agg + self.update(F.silu(agg))

    def forward(self, source, src_pos, dst_pos):
        d2 = (dst_pos[:,:,None]-src_pos[:,None]).square().sum(-1)
        weights = self.scores(d2).softmax(-1)
        return self.finish(weights @ self.transform(source))

    def sparse(self, source, pos, edges):
        """The same learned block supports the published irregular superpixel neighborhoods."""
        src,dst = edges
        score = self.scores((pos[src]-pos[dst]).square().sum(-1))
        maxima = score.new_full((len(pos),), -torch.inf)
        maxima.scatter_reduce_(0,dst,score.detach(),reduce="amax")
        exp = (score-maxima[dst]).exp()
        denom = exp.new_zeros(len(pos)).index_add_(0,dst,exp)
        weight = exp / denom[dst].clamp_min(1e-12)
        agg = source.new_zeros(source.shape).index_add_(0,dst,self.transform(source)[src]*weight[:,None])
        return self.finish(agg)


class SceneClassifier(nn.Module):
    """Output one scene logit from observable features and two learned geometric hops."""
    def __init__(self, kind="cd32", seed=0):
        super().__init__()
        if kind not in KINDS:
            raise ValueError(f"unknown model {kind}")
        self.kind = kind
        rule = kind if kind in ("cd32","random","real","budget","cd16") else "cd32"
        if kind == "shallow":
            self.point = nn.Sequential(nn.Linear(32+32+1+2+3,64),nn.SiLU(),nn.Linear(64,WIDTH))
            self.head = nn.Sequential(nn.Linear(WIDTH,WIDTH),nn.SiLU(),nn.Linear(WIDTH,1))
            return
        self.sensor = Sensor(rule,seed)
        self.landmark = DistanceBlock(rule,seed)
        self.beacon = DistanceBlock(rule,seed)
        self.head = nn.Sequential(nn.Linear(2*WIDTH,WIDTH),nn.SiLU(),nn.Linear(WIDTH,1))
        if kind == "frozen":
            for module in (self.sensor,self.landmark,self.beacon):
                module.requires_grad_(False)

    def forward(self, f):
        if self.kind == "shallow":
            # A global-access permutation-invariant set model sees positions, roles and readings.
            pos = torch.cat((f["pos"],f["land"],f["beacon"]),1)
            raw = torch.cat((f["x"],F.one_hot(f["k"],32).to(pos.dtype),f["z"][...,None]),-1)
            raw = F.pad(raw,(0,0,0,pos.shape[1]-raw.shape[1]))
            roles = torch.cat([pos.new_full((v.shape[1],),i,dtype=torch.long)
                               for i,v in enumerate((f["pos"],f["land"],f["beacon"]))])
            role = F.one_hot(roles,3).expand(len(pos),-1,-1)
            h = self.point(torch.cat((raw,pos,role),-1)).mean(1)
            return self.head(h).squeeze(-1)
        obj = self.sensor(f["x"],f["k"],f["z"])
        if self.kind == "onehop":
            marks = obj.new_zeros((len(obj),f["land"].shape[1],WIDTH))
        else:
            marks = self.landmark(obj,f["pos"],f["land"])
        h = self.beacon(marks,f["land"],f["beacon"])
        # Symmetric sum and second-order interaction admit arbitrary learned same/different readouts.
        summary = torch.cat((h.sum(1),h[:,0]*h[:,1]),-1)
        return self.head(summary).squeeze(-1)
