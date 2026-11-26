# scene-cd32-cd32-s5-n1024

scene / cd32 / cd32 / 1024 families. Seed 5, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 31. Validation accuracy was 90.82% and test accuracy was 90.77%. Both mates were correct in 85.16% of families. The oracle scored 94.73%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-cd32-cd32-s5-n1024 | 3801 | 90.82% | 90.77% | 85.16% | 89.70% | 88.62% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 22.0 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision d99f5908cb66b6c617458e2e1f17763ccce1cce8.

[Manifest](../../../results/scene-cd32-cd32-s5-n1024/train.json) · [Epoch log](../../../logs/scene-cd32-cd32-s5-n1024.jsonl) · [Protocol](../../preregistration.md)
