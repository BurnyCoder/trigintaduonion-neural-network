# scene-budget-cd32-s1-n1024

scene / budget / cd32 / 1024 families. Seed 1, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 36. Validation accuracy was 53.32% and test accuracy was 50.93%. Both mates were correct in 23.05% of families. The oracle scored 93.41%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-budget-cd32-s1-n1024 | 3961 | 53.32% | 50.93% | 23.05% | 51.32% | 48.34% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 16.9 epoch-loop seconds. Peak allocated device memory was 38,914,048 bytes. Source revision 62ad26663b72f5ec8a8d6b7a26df13ed02b7ac6e.

[Manifest](../../../results/scene-budget-cd32-s1-n1024/train.json) · [Epoch log](../../../logs/scene-budget-cd32-s1-n1024.jsonl) · [Protocol](../../preregistration.md)
