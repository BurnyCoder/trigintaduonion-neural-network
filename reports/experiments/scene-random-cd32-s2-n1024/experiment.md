# scene-random-cd32-s2-n1024

scene / random / cd32 / 1024 families. Seed 2, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 32. Validation accuracy was 53.32% and test accuracy was 49.46%. Both mates were correct in 21.78% of families. The oracle scored 93.51%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-random-cd32-s2-n1024 | 3801 | 53.32% | 49.46% | 21.78% | 49.17% | 49.85% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 24.2 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision eb6fe01cc39c73c25cf1483650ab242e4b0b82e3.

[Manifest](../../../results/scene-random-cd32-s2-n1024/train.json) · [Epoch log](../../../logs/scene-random-cd32-s2-n1024.jsonl) · [Protocol](../../preregistration.md)
