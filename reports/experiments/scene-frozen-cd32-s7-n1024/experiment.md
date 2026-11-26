# scene-frozen-cd32-s7-n1024

scene / frozen / cd32 / 1024 families. Seed 7, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 11. Validation accuracy was 53.52% and test accuracy was 50.49%. Both mates were correct in 15.82% of families. The oracle scored 93.36%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-frozen-cd32-s7-n1024 | 2113 | 53.52% | 50.49% | 15.82% | 48.73% | 51.32% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 13.1 epoch-loop seconds. Peak allocated device memory was 37,708,800 bytes. Source revision df26e3ff08034bc4795c2e9a315bb47b790a913c.

[Manifest](../../../results/scene-frozen-cd32-s7-n1024/train.json) · [Epoch log](../../../logs/scene-frozen-cd32-s7-n1024.jsonl) · [Protocol](../../preregistration.md)
