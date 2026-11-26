"""Tests connect the algebra, observable scenes and trainable spatial processor."""
import numpy as np
import pytest
import torch

from trig32.algebra import CD32Conv2d, CD32Linear, basis_signs, cd32_mul, randomize
from trig32.reference import oracle_signs
from trig32.scenes import SceneSet
from trig32.models import SceneClassifier


def test_all_ordered_products_and_triples():
    """Each independently evaluated basis product must have the expected location and sign."""
    eye = torch.eye(32, dtype=torch.float64)
    actual = cd32_mul(eye[:, None], eye[None, :])
    idx = np.arange(32)
    expected = eye[idx[:, None] ^ idx] * torch.tensor(oracle_signs())[:, :, None]
    torch.testing.assert_close(actual, expected)
    control = randomize(basis_signs(32), 7)
    np.testing.assert_array_equal(control[:16, :16], oracle_signs()[:16, :16])
    assert np.count_nonzero(control != oracle_signs()) == 60 * 6
    a, b, c = eye[[1, 2, 4]]
    assert not torch.equal(cd32_mul(cd32_mul(a, b), c), cd32_mul(a, cd32_mul(b, c)))
    assert not cd32_mul(eye[3] + eye[10], eye[6] - eye[15]).any()


def test_linear_conv_and_autograd():
    """A one-tap convolution and dense left product share all component and group ordering."""
    x = torch.randn(2, 2, 32, dtype=torch.double, requires_grad=True)
    lin = CD32Linear(2, 3, bias=False).double()
    conv = CD32Conv2d(2, 3, 1, bias=False).double()
    with torch.no_grad():
        conv.weight.copy_(lin.weight[..., None, None])
    expected = cd32_mul(lin.weight[None], x[:, None]).sum(2)
    torch.testing.assert_close(lin(x), expected)
    torch.testing.assert_close(conv(x.reshape(2, 64, 1, 1)).reshape(2, 3, 32), expected)
    from torch.func import functional_call
    assert torch.autograd.gradcheck(lambda v, w: functional_call(lin, {"weight": w}, (v,)),
                                    (x, lin.weight), fast_mode=True)


def test_swapped_mates_and_disjoint_streams():
    """The source, nuisance draws and graph layout pair across renderers and mates."""
    ds = SceneSet(14, 5, "train", "cd32")
    alt = SceneSet(14, 5, "train", "random")
    ids = torch.arange(len(ds))
    f, y = ds.batch(ids)
    g, v = alt.batch(ids)
    assert torch.equal(y[::2], 1 - y[1::2])
    for key in ("pos", "land", "beacon"):
        assert torch.equal(f[key][::2], f[key][1::2])
    assert torch.equal(f["x"], g["x"]) and torch.equal(y, v)
    assert not torch.equal(f["z"], g["z"])
    assert torch.equal(f["z"][::2].sort(1).values, f["z"][1::2].sort(1).values)
    assert set(f["k"].flatten().tolist()).isdisjoint({12,13,14,15,28,29,30,31})
    assert not torch.equal(ds.batch(ids)[0]["x"], SceneSet(14,5,"val","cd32").batch(ids)[0]["x"])


@pytest.mark.parametrize("kind", ["cd32", "random", "real", "budget", "cd16", "frozen", "onehop", "shallow"])
def test_full_classifier_and_isometries(kind):
    """Spatial symmetries apply to the geometric processor and gradients reach its trainable head."""
    f, y = SceneSet(4, 17, "val", "cd32").batch(torch.arange(8))
    model = SceneClassifier(kind, 17)
    out = model(f)
    assert out.shape == y.shape
    torch.nn.functional.binary_cross_entropy_with_logits(out, y).backward()
    assert any(p.grad is not None for p in model.parameters())
    if kind == "shallow":
        return
    transform = torch.tensor([[0., 1.], [1., 0.]])
    changed = {**f, **{key: f[key] @ transform + 3 for key in ("pos", "land", "beacon")}}
    for key in ("pos", "x", "k", "z"):
        changed[key] = changed[key].flip(1)
    changed["land"] = changed["land"].flip(1)
    changed["beacon"] = changed["beacon"].flip(1)
    torch.testing.assert_close(out, model(changed), atol=3e-5, rtol=2e-5)
    if kind == "onehop":
        torch.testing.assert_close(out[::2], out[1::2])


@pytest.mark.skipif(not torch.cuda.is_available(), reason="requires CUDA")
def test_cuda_forward_and_backward():
    """Compare CPU and device outputs plus gradients on the same weights and observations."""
    import copy
    f, _ = SceneSet(3, 3, "train", "cd32").batch(torch.arange(6))
    cpu = SceneClassifier("cd32", 3)
    gpu = copy.deepcopy(cpu).cuda()
    left, right = cpu(f), gpu({k:v.cuda() for k,v in f.items()})
    torch.testing.assert_close(left, right.cpu(), atol=1e-4, rtol=1e-4)
    left.sum().backward()
    right.sum().backward()
    for a,b in zip(cpu.parameters(), gpu.parameters()):
        if a.grad is not None:
            torch.testing.assert_close(a.grad, b.grad.cpu(), atol=3e-4, rtol=3e-4)
