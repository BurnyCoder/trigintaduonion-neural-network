"""The actual equality objective must send a finite gradient through each learned stage."""
import torch
from trig32.models import SceneClassifier
from trig32.scenes import SceneSet


def test_scene_supervision_reaches_every_stage():
    torch.manual_seed(73)
    f,y=SceneSet(8,73,"val","cd32").batch(torch.arange(16))
    model=SceneClassifier()
    torch.nn.functional.binary_cross_entropy_with_logits(model(f),y).backward()
    for module in (model.sensor.mix,model.sensor.encode,model.landmark.value,model.landmark.update,
                   model.landmark.gate,model.beacon.value,model.beacon.update,model.beacon.gate,model.head):
        gradients=[p.grad for p in module.parameters() if p.grad is not None]
        assert gradients and all(g.isfinite().all() for g in gradients)
        assert any(g.count_nonzero() for g in gradients)
