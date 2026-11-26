# scene-random-random-s4-n1024

scene / random / random / 1024 families. Seed 4, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 36. Validation accuracy was 88.67% and test accuracy was 89.70%. Both mates were correct in 83.11% of families. The oracle scored 93.51%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-random-random-s4-n1024 | 3801 | 88.67% | 89.70% | 83.11% | 89.26% | 87.55% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 24.3 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision 69bdf8caaf2ccc33fc20bc0fd9df63db2dbc6e3f.

[Manifest](../../../results/scene-random-random-s4-n1024/train.json) · [Epoch log](../../../logs/scene-random-random-s4-n1024.jsonl) · [Protocol](../../preregistration.md)
