# scene-cd16-cd32-s2-n1024

scene / cd16 / cd32 / 1024 families. Seed 2, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 40. Validation accuracy was 56.05% and test accuracy was 55.91%. Both mates were correct in 30.66% of families. The oracle scored 93.51%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-cd16-cd32-s2-n1024 | 4057 | 56.05% | 55.91% | 30.66% | 56.98% | 54.93% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 20.0 epoch-loop seconds. Peak allocated device memory was 38,923,776 bytes. Source revision c20dda33ffe8fabd1dee2e3ebeff4dd007b3abfd.

[Manifest](../../../results/scene-cd16-cd32-s2-n1024/train.json) · [Epoch log](../../../logs/scene-cd16-cd32-s2-n1024.jsonl) · [Protocol](../../preregistration.md)
