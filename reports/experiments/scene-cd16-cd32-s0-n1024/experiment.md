# scene-cd16-cd32-s0-n1024

scene / cd16 / cd32 / 1024 families. Seed 0, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 53. Validation accuracy was 63.67% and test accuracy was 63.53%. Both mates were correct in 41.70% of families. The oracle scored 93.95%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-cd16-cd32-s0-n1024 | 4057 | 63.67% | 63.53% | 41.70% | 62.99% | 63.96% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 22.1 epoch-loop seconds. Peak allocated device memory was 38,923,776 bytes. Source revision ae8fe2d29613b794976524e2b82fa0bf96526b25.

[Manifest](../../../results/scene-cd16-cd32-s0-n1024/train.json) · [Epoch log](../../../logs/scene-cd16-cd32-s0-n1024.jsonl) · [Protocol](../../preregistration.md)
