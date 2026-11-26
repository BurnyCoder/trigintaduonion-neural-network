# scene-cd32-cd32-s0-n256

scene / cd32 / cd32 / 256 families. Seed 0, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 59. Validation accuracy was 57.03% and test accuracy was 56.10%. Both mates were correct in 31.93% of families. The oracle scored 93.95%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-cd32-cd32-s0-n256 | 3801 | 57.03% | 56.10% | 31.93% | 60.21% | 59.23% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 8.8 epoch-loop seconds. Peak allocated device memory was 37,044,736 bytes. Source revision 4b2bf8b142989656e64d8b33073bd9a7a75c8a59.

[Manifest](../../../results/scene-cd32-cd32-s0-n256/train.json) · [Epoch log](../../../logs/scene-cd32-cd32-s0-n256.jsonl) · [Protocol](../../preregistration.md)
