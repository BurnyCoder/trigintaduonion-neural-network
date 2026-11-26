# scene-random-cd32-s1-n1024

scene / random / cd32 / 1024 families. Seed 1, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 40. Validation accuracy was 56.84% and test accuracy was 49.27%. Both mates were correct in 24.32% of families. The oracle scored 93.41%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-random-cd32-s1-n1024 | 3801 | 56.84% | 49.27% | 24.32% | 48.93% | 49.66% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 23.8 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision bd48bf0763fe1d1d62963b553e60a108661a2781.

[Manifest](../../../results/scene-random-cd32-s1-n1024/train.json) · [Epoch log](../../../logs/scene-random-cd32-s1-n1024.jsonl) · [Protocol](../../preregistration.md)
