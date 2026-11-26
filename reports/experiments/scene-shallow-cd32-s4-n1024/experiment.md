# scene-shallow-cd32-s4-n1024

scene / shallow / cd32 / 1024 families. Seed 4, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 43. Validation accuracy was 50.20% and test accuracy was 50.00%. Both mates were correct in 0.20% of families. The oracle scored 93.16%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-shallow-cd32-s4-n1024 | 7713 | 50.20% | 50.00% | 0.20% | 49.90% | 50.05% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 7.4 epoch-loop seconds. Peak allocated device memory was 39,115,776 bytes. Source revision c08e65635397942148c67758a6f14669e7a1c2a2.

[Manifest](../../../results/scene-shallow-cd32-s4-n1024/train.json) · [Epoch log](../../../logs/scene-shallow-cd32-s4-n1024.jsonl) · [Protocol](../../preregistration.md)
