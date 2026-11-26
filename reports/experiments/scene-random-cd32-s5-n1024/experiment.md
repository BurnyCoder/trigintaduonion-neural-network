# scene-random-cd32-s5-n1024

scene / random / cd32 / 1024 families. Seed 5, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 15. Validation accuracy was 55.47% and test accuracy was 50.68%. Both mates were correct in 24.61% of families. The oracle scored 94.73%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-random-cd32-s5-n1024 | 3801 | 55.47% | 50.68% | 24.61% | 51.56% | 50.10% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 21.5 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision f484d5689390fe5aa3a9216619da464999b78f09.

[Manifest](../../../results/scene-random-cd32-s5-n1024/train.json) · [Epoch log](../../../logs/scene-random-cd32-s5-n1024.jsonl) · [Protocol](../../preregistration.md)
