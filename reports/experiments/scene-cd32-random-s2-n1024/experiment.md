# scene-cd32-random-s2-n1024

scene / cd32 / random / 1024 families. Seed 2, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 37. Validation accuracy was 57.62% and test accuracy was 50.10%. Both mates were correct in 23.14% of families. The oracle scored 93.80%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-cd32-random-s2-n1024 | 3801 | 57.62% | 50.10% | 23.14% | 49.80% | 49.41% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 26.3 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision 29338fb2d1c43caa1a7f04e8dbf3397262805607.

[Manifest](../../../results/scene-cd32-random-s2-n1024/train.json) · [Epoch log](../../../logs/scene-cd32-random-s2-n1024.jsonl) · [Protocol](../../preregistration.md)
