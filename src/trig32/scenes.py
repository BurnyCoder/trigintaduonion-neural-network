"""Generate group-disjoint counterfactual scenes. Only observable tensors enter the model."""
import numpy as np
import torch

from .reference import left_matrix, reference_table

SPLITS = {"train": 1, "val": 2, "test": 3, "heldout": 4, "crowded": 5}
RESERVED = np.array([12, 13, 14, 15, 28, 29, 30, 31])
SUPPORTED = np.setdiff1d(np.arange(32), RESERVED)


def filter_vector(seed):
    """Sample a reproducible pure-imaginary filter with exactly balanced subalgebra energy."""
    rng = np.random.default_rng(np.random.SeedSequence([seed, 101]))
    w = rng.standard_normal(32)
    w[0] = 0
    halves = w.reshape(2, 16)
    halves /= np.sqrt(2) * np.linalg.norm(halves, axis=1, keepdims=True)
    return w.astype(np.float32)


def geometry(rng, size, objects):
    """Rejection-sample separated nearest-neighbor choices on independent uniform layouts."""
    accepted = []
    remaining = size
    while remaining:
        p = rng.random((max(64, 4*remaining), 6 + objects, 2), dtype=np.float32)
        beacons, lands, obs = p[:, :2], p[:, 2:6], p[:, 6:]
        d1 = np.linalg.norm(beacons[:, :, None] - lands[:, None], axis=-1)
        d2 = np.linalg.norm(lands[:, :, None] - obs[:, None], axis=-1)
        near_land = d1.argmin(-1)
        row = np.arange(len(p))[:, None]
        candidates = d2[row, near_land]
        selected = candidates.argmin(-1)
        # A visible margin makes the ideal spatial selection robust to position rounding.
        first_two = np.partition(d1, 1, axis=-1)[..., :2]
        next_two = np.partition(candidates, 1, axis=-1)[..., :2]
        keep = ((near_land[:,0] != near_land[:,1]) & (selected[:,0] != selected[:,1])
                & (first_two.max(-1)-first_two.min(-1) > .035).all(1)
                & (next_two.max(-1)-next_two.min(-1) > .035).all(1))
        choose = np.flatnonzero(keep)[:remaining]
        accepted.append((p[choose], selected[choose]))
        remaining -= len(choose)
    return tuple(np.concatenate(part) for part in zip(*accepted))


def _chunk(seed, split, block, objects, matrix):
    """Fixed-size keyed chunks guarantee nested sample sizes and paired renderer worlds."""
    rng = np.random.default_rng(np.random.SeedSequence([seed, SPLITS[split], 102, block]))
    size = 256
    coords, sel = geometry(rng, size, objects)
    row = np.arange(size)
    types = np.where(np.argsort(rng.random((size,objects)), axis=1) < objects//2, 1, -1)
    target = (types[row, sel[:,0]] == types[row, sel[:,1]]).astype(np.float32)
    pick = sel[row, rng.integers(2, size=size)]
    eligible = types != types[row,pick,None]
    eligible[row[:,None],sel] = False
    swap = np.where(eligible, rng.random(eligible.shape), -1).argmax(1)
    perm = np.broadcast_to(np.arange(objects), (size,objects)).copy()
    perm[row,pick], perm[row,swap] = swap, pick
    x = rng.standard_normal((size,objects,32), dtype=np.float32)
    k = rng.choice(RESERVED if split=="heldout" else SUPPORTED, size=(size,objects))
    z = (types * (matrix[k] * x).sum(-1) + .1*rng.standard_normal((size,objects))).astype(np.float32)
    f = {"beacon":coords[:,:2], "land":coords[:,2:6], "pos":coords[:,6:]}
    f = {name:np.repeat(v,2,axis=0) for name,v in f.items()}
    for name,v in {"x":x, "k":k, "z":z}.items():
        f[name] = np.stack((v, v[row[:,None],perm]), axis=1).reshape(-1,*v.shape[1:])
    return f, np.stack((target,1-target),axis=1).ravel()


class SceneSet:
    """A fixed split of parent scenes, with each original immediately followed by its mate."""
    def __init__(self, families, seed, split, rule, device="cpu"):
        if split not in SPLITS or families < 1:
            raise ValueError("specify a known split and at least one family")
        self.rule, self.seed, self.families = rule,seed,families
        self.matrix = left_matrix(filter_vector(seed), reference_table(rule, seed))
        chunks = [_chunk(seed, split, i, 16 if split=="crowded" else 8, self.matrix)
                  for i in range((families+255)//256)]
        self.features = {k:torch.from_numpy(np.concatenate([f[k] for f,_ in chunks])[:2*families]).to(device)
                         for k in chunks[0][0]}
        self.y = torch.from_numpy(np.concatenate([y for _,y in chunks])[:2*families]).to(device)

    def __len__(self):
        return len(self.y)

    def batch(self, indices):
        return {k:v[indices] for k,v in self.features.items()}, self.y[indices]

    def oracle(self, f):
        """Privileged analytic diagnostic. It knows the filter and computes the two selections."""
        ids = torch.cdist(f["beacon"], f["land"]).argmin(-1)
        obj = torch.cdist(f["land"], f["pos"]).argmin(-1).gather(1,ids)
        mat = torch.as_tensor(self.matrix, device=f["x"].device)
        evidence = (mat[f["k"]]*f["x"]).sum(-1)*f["z"]
        bits = evidence.gather(1,obj) > 0
        return (bits[:,0] == bits[:,1]).float()
