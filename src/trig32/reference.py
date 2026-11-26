"""Independent data-side multiplication. No trained PyTorch layer is called here."""
from functools import lru_cache
import numpy as np

from .algebra import randomize
from .paths import DATA


@lru_cache(maxsize=1)
def oracle_signs():
    """Evaluate every scalar library basis product once, caching the integer answer locally.

    https://github.com/discretegames/hypercomplex/tree/d026ee205a4bf41f93b5c67df17e212ca3be5de2
    """
    import os
    from tempfile import NamedTemporaryFile
    from hypercomplex import CD32
    path = DATA / "oracle-hypercomplex-0.3.4.npy"
    if path.exists():
        return np.load(path, allow_pickle=False)
    basis = [CD32.e(i) for i in range(32)]
    table = np.empty((32,32), dtype=np.int8)
    for i, a in enumerate(basis):
        for j, b in enumerate(basis):
            coeff = np.asarray((a * b).coefficients())
            k = i ^ j
            if np.count_nonzero(coeff) != 1 or abs(coeff[k]) != 1:
                raise ArithmeticError(f"unexpected scalar reference at {i},{j}")
            table[i,j] = coeff[k]
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=path.parent, suffix=".tmp", delete=False) as f:
        np.save(f, table)
    os.replace(f.name, path)
    return table


def reference_table(rule, seed):
    """Both worlds use the same published scalar convention and registered intervention."""
    table = oracle_signs()
    return randomize(table, seed) if rule == "random" else table


def left_matrix(w, table):
    """Build the real matrix of w times an input by assigning each basis product into its output."""
    i, j = np.indices(table.shape)
    out = np.empty_like(table, dtype=w.dtype)
    out[i ^ j, j] = w[i] * table[i,j]
    return out


def products(x, y, table):
    """Accumulate batched reference products over left basis indices without a dense 3-tensor."""
    ids = np.arange(32)
    output = np.zeros(np.broadcast_shapes(x.shape, y.shape), dtype=np.result_type(x,y))
    for i in ids:
        output[..., i ^ ids] += x[..., i, None] * y * table[i]
    return output
