# scene-cd32-random-s1-n1024

scene / cd32 / random / 1024 families. Seed 1, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 20. Validation accuracy was 58.79% and test accuracy was 50.68%. Both mates were correct in 24.02% of families. The oracle scored 93.90%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-cd32-random-s1-n1024 | 3801 | 58.79% | 50.68% | 24.02% | 51.90% | 50.54% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 22.4 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision a12e6e87e543adc57d7ed82c80a45f5230bb9352.

[Manifest](../../../results/scene-cd32-random-s1-n1024/train.json) · [Epoch log](../../../logs/scene-cd32-random-s1-n1024.jsonl) · [Protocol](../../preregistration.md)
