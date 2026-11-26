"""Left Cayley–Dickson products expanded as signed real kernels.

Definition 2.1 of Biss, Dugger and Isaksen: https://arxiv.org/pdf/math/0511691
Basis routing follows the XOR relation in https://arxiv.org/pdf/1405.6888 .
"""
from functools import lru_cache
import math

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F


@lru_cache(maxsize=None)
def basis_signs(n):
    """Derive one sign for each ordered pair using (ac-d*b, da+bc*)."""
    if n < 1 or n & (n - 1):
        raise ValueError("the Cayley–Dickson dimension must be a power of two")
    if n == 1:
        return np.ones((1, 1), dtype=np.int8)
    half = n // 2
    previous = basis_signs(half)
    conj = np.where(np.arange(half) == 0, 1, -1).astype(np.int8)
    # Upper/upper left operands contribute -conj(d)b; mixed blocks use da or b conj(c).
    return np.block([[previous, previous.T], [previous * conj, -previous.T * conj]])


def randomize(signs, seed):
    """Reverse a fixed-size random subset of upper triples, preserving both operand orders."""
    n = len(signs)
    triples = [(a, b, a ^ b) for a in range(1, n) for b in range(a + 1, n)
               if b < (a ^ b) and (a ^ b) >= n // 2]
    rng = np.random.default_rng(np.random.SeedSequence([seed, 610]))
    result = signs.copy()
    for i in rng.choice(len(triples), len(triples) // 2, replace=False):
        a,b,c = triples[i]
        result[[a,b,b,c,c,a], [b,a,c,b,a,c]] *= -1
    return result


def rule_signs(name, seed=0, n=32):
    """Return canonical or randomized signs in fixed basis order."""
    if name not in ("cd32", "random", "cd16"):
        raise ValueError(f"unknown multiplication rule {name}")
    table = basis_signs(n)
    return randomize(table, seed) if name == "random" else table


def routing(signs):
    """Index by output basis and input basis to retrieve the weight component and its sign."""
    ids = np.arange(len(signs))
    weights = ids[:, None] ^ ids[None, :]
    return torch.from_numpy(weights), torch.from_numpy(signs[weights, ids])


def cd32_mul(x, y):
    """Multiply broadcasting real tensors whose final dimension stores 32 ordered coefficients."""
    if x.shape[-1] != 32 or y.shape[-1] != 32:
        raise ValueError("both operands need a final component axis of length 32")
    idx, signs = routing(basis_signs(32))
    return (x[..., idx.to(x.device)] * signs.to(x.device) * y.unsqueeze(-2)).sum(-1)


class _LeftKernel(nn.Module):
    """One weight group generates a full matrix of real channel interactions per kernel tap."""
    def __init__(self, ins, outs, spatial=(), *, rule="cd32", seed=0, bias=True):
        super().__init__()
        self.n = 16 if rule == "cd16" else 32
        self.ins, self.outs = ins, outs
        self.weight = nn.Parameter(torch.empty(outs, ins, self.n, *spatial))
        self.bias = nn.Parameter(torch.zeros(outs * self.n)) if bias else None
        index, sign = routing(rule_signs(rule, seed, self.n))
        self.register_buffer("index", index)
        self.register_buffer("sign", sign)
        bound = 1 / math.sqrt(ins * self.n * math.prod(spatial))
        nn.init.uniform_(self.weight, -bound, bound)

    def expanded(self):
        """Gather tied coefficients, then flatten group and basis axes in channel-major order."""
        spatial = self.weight.shape[3:]
        sign = self.sign.reshape(self.n, self.n, *([1] * len(spatial)))
        expanded = (self.weight[:, :, self.index] * sign).transpose(1, 2)
        return expanded.reshape(self.outs * self.n, self.ins * self.n, *spatial)


class CD32Linear(_LeftKernel):
    """Map (..., input_groups, basis) into (..., output_groups, basis)."""
    def forward(self, x):
        if x.shape[-2:] != (self.ins, self.n):
            raise ValueError(f"expected group and basis shape {(self.ins, self.n)}")
        return F.linear(x.flatten(-2), self.expanded(), self.bias).unflatten(-1, (self.outs, self.n))


class CD32Conv2d(_LeftKernel):
    """NCHW convolution with consecutive components within each hypercomplex channel."""
    def __init__(self, ins, outs, kernel_size, *, stride=1, padding=0, **kwargs):
        super().__init__(ins, outs, (kernel_size, kernel_size), **kwargs)
        self.stride, self.padding = stride, padding

    def forward(self, x):
        return F.conv2d(x, self.expanded(), self.bias, self.stride, self.padding)
