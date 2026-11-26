# scene-shallow-cd32-s2-n1024

scene / shallow / cd32 / 1024 families. Seed 2, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 58. Validation accuracy was 50.59% and test accuracy was 50.05%. Both mates were correct in 0.20% of families. The oracle scored 93.51%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-shallow-cd32-s2-n1024 | 7713 | 50.59% | 50.05% | 0.20% | 50.00% | 50.00% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 7.4 epoch-loop seconds. Peak allocated device memory was 39,115,776 bytes. Source revision 24f6ae018ad867619903b6152be60d15292fb077.

[Manifest](../../../results/scene-shallow-cd32-s2-n1024/train.json) · [Epoch log](../../../logs/scene-shallow-cd32-s2-n1024.jsonl) · [Protocol](../../preregistration.md)
