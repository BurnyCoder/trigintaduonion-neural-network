# scene-cd32-random-s7-n1024

scene / cd32 / random / 1024 families. Seed 7, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 7. Validation accuracy was 54.30% and test accuracy was 49.85%. Both mates were correct in 19.04% of families. The oracle scored 94.63%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-cd32-random-s7-n1024 | 3801 | 54.30% | 49.85% | 19.04% | 49.32% | 51.90% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 30.8 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision dc260acf708fb59bc6320aaf067e4605e45ed633.

[Manifest](../../../results/scene-cd32-random-s7-n1024/train.json) · [Epoch log](../../../logs/scene-cd32-random-s7-n1024.jsonl) · [Protocol](../../preregistration.md)
