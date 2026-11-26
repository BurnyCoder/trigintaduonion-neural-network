# scene-cd32-random-s5-n1024

scene / cd32 / random / 1024 families. Seed 5, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 58. Validation accuracy was 51.76% and test accuracy was 50.39%. Both mates were correct in 24.71% of families. The oracle scored 94.97%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-cd32-random-s5-n1024 | 3801 | 51.76% | 50.39% | 24.71% | 50.00% | 49.17% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 22.5 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision 408791df9aa6f0ff4a24cfb588fa8f07ad8b18f7.

[Manifest](../../../results/scene-cd32-random-s5-n1024/train.json) · [Epoch log](../../../logs/scene-cd32-random-s5-n1024.jsonl) · [Protocol](../../preregistration.md)
