# scene-shallow-cd32-s5-n1024

scene / shallow / cd32 / 1024 families. Seed 5, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 1. Validation accuracy was 50.39% and test accuracy was 49.95%. Both mates were correct in 0.10% of families. The oracle scored 94.73%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-shallow-cd32-s5-n1024 | 7713 | 50.39% | 49.95% | 0.10% | 49.95% | 49.90% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 7.4 epoch-loop seconds. Peak allocated device memory was 39,115,776 bytes. Source revision 20d549901f55d09b54b5722f874dc62c6c1ae27c.

[Manifest](../../../results/scene-shallow-cd32-s5-n1024/train.json) · [Epoch log](../../../logs/scene-shallow-cd32-s5-n1024.jsonl) · [Protocol](../../preregistration.md)
