# scene-shallow-cd32-s7-n1024

scene / shallow / cd32 / 1024 families. Seed 7, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 78. Validation accuracy was 50.20% and test accuracy was 49.80%. Both mates were correct in 0.10% of families. The oracle scored 93.36%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-shallow-cd32-s7-n1024 | 7713 | 50.20% | 49.80% | 0.10% | 50.05% | 49.95% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 7.4 epoch-loop seconds. Peak allocated device memory was 39,115,776 bytes. Source revision 8483a05cf206c046a099861dfaa04b08e28146a9.

[Manifest](../../../results/scene-shallow-cd32-s7-n1024/train.json) · [Epoch log](../../../logs/scene-shallow-cd32-s7-n1024.jsonl) · [Protocol](../../preregistration.md)
