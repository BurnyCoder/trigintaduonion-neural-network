# scene-random-random-s7-n1024

scene / random / random / 1024 families. Seed 7, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 35. Validation accuracy was 92.19% and test accuracy was 89.70%. Both mates were correct in 82.13% of families. The oracle scored 94.63%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-random-random-s7-n1024 | 3801 | 92.19% | 89.70% | 82.13% | 89.79% | 90.04% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 29.7 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision 762847379251bcbccfd62eec09a29819ccd0204c.

[Manifest](../../../results/scene-random-random-s7-n1024/train.json) · [Epoch log](../../../logs/scene-random-random-s7-n1024.jsonl) · [Protocol](../../preregistration.md)
