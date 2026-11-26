# scene-shallow-cd32-s1-n1024

scene / shallow / cd32 / 1024 families. Seed 1, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 24. Validation accuracy was 50.20% and test accuracy was 50.00%. Both mates were correct in 0.39% of families. The oracle scored 93.41%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-shallow-cd32-s1-n1024 | 7713 | 50.20% | 50.00% | 0.39% | 49.95% | 49.90% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 7.6 epoch-loop seconds. Peak allocated device memory was 39,115,776 bytes. Source revision 5e214d1cf9dba3c78819e9d193ed7c56fd67787a.

[Manifest](../../../results/scene-shallow-cd32-s1-n1024/train.json) · [Epoch log](../../../logs/scene-shallow-cd32-s1-n1024.jsonl) · [Protocol](../../preregistration.md)
