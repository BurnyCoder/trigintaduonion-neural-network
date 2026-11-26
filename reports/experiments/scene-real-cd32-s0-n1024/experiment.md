# scene-real-cd32-s0-n1024

scene / real / cd32 / 1024 families. Seed 0, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 23. Validation accuracy was 56.64% and test accuracy was 50.44%. Both mates were correct in 23.34% of families. The oracle scored 93.95%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-real-cd32-s0-n1024 | 11737 | 56.64% | 50.44% | 23.34% | 49.46% | 50.83% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 17.0 epoch-loop seconds. Peak allocated device memory was 38,983,680 bytes. Source revision 69111a2a33da7675ca437525efbaf652d32ff180.

[Manifest](../../../results/scene-real-cd32-s0-n1024/train.json) · [Epoch log](../../../logs/scene-real-cd32-s0-n1024.jsonl) · [Protocol](../../preregistration.md)
