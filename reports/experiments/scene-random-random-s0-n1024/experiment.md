# scene-random-random-s0-n1024

scene / random / random / 1024 families. Seed 0, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 37. Validation accuracy was 89.84% and test accuracy was 89.99%. Both mates were correct in 83.69% of families. The oracle scored 93.55%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-random-random-s0-n1024 | 3801 | 89.84% | 89.99% | 83.69% | 90.58% | 89.11% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 30.9 epoch-loop seconds. Peak allocated device memory was 39,038,464 bytes. Source revision 1240f949e4750166b2090ed541b7710af67a3a73.

[Manifest](../../../results/scene-random-random-s0-n1024/train.json) · [Epoch log](../../../logs/scene-random-random-s0-n1024.jsonl) · [Protocol](../../preregistration.md)
