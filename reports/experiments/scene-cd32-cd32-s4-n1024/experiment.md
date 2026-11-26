# scene-cd32-cd32-s4-n1024

scene / cd32 / cd32 / 1024 families. Seed 4, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 30. Validation accuracy was 90.62% and test accuracy was 88.62%. Both mates were correct in 80.08% of families. The oracle scored 93.16%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-cd32-cd32-s4-n1024 | 3801 | 90.62% | 88.62% | 80.08% | 89.40% | 87.40% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 22.2 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision f4bb03cf80674da4b0afaa426380046687f7fd87.

[Manifest](../../../results/scene-cd32-cd32-s4-n1024/train.json) · [Epoch log](../../../logs/scene-cd32-cd32-s4-n1024.jsonl) · [Protocol](../../preregistration.md)
