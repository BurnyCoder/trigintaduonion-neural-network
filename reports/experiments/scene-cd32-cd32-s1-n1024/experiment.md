# scene-cd32-cd32-s1-n1024

scene / cd32 / cd32 / 1024 families. Seed 1, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 59. Validation accuracy was 90.43% and test accuracy was 89.16%. Both mates were correct in 81.74% of families. The oracle scored 93.41%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-cd32-cd32-s1-n1024 | 3801 | 90.43% | 89.16% | 81.74% | 88.92% | 88.23% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 23.3 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision 98bdb752a4f324174b90ef99648b7d49afa46ee3.

[Manifest](../../../results/scene-cd32-cd32-s1-n1024/train.json) · [Epoch log](../../../logs/scene-cd32-cd32-s1-n1024.jsonl) · [Protocol](../../preregistration.md)
