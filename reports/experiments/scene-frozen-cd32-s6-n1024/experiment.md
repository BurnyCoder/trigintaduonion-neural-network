# scene-frozen-cd32-s6-n1024

scene / frozen / cd32 / 1024 families. Seed 6, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 20. Validation accuracy was 54.49% and test accuracy was 51.03%. Both mates were correct in 11.82% of families. The oracle scored 94.14%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-frozen-cd32-s6-n1024 | 2113 | 54.49% | 51.03% | 11.82% | 50.83% | 49.90% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 14.9 epoch-loop seconds. Peak allocated device memory was 37,708,800 bytes. Source revision 219cfe20828a7263eef4510cdf875d0adb0370b9.

[Manifest](../../../results/scene-frozen-cd32-s6-n1024/train.json) · [Epoch log](../../../logs/scene-frozen-cd32-s6-n1024.jsonl) · [Protocol](../../preregistration.md)
