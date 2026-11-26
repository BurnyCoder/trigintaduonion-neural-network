# scene-cd32-cd32-s7-n1024

scene / cd32 / cd32 / 1024 families. Seed 7, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 70. Validation accuracy was 92.38% and test accuracy was 90.53%. Both mates were correct in 85.16% of families. The oracle scored 93.36%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-cd32-cd32-s7-n1024 | 3801 | 92.38% | 90.53% | 85.16% | 91.06% | 90.53% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 32.0 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision 9a51ee04fdeb01c7cc74f922f91e521062dc1091.

[Manifest](../../../results/scene-cd32-cd32-s7-n1024/train.json) · [Epoch log](../../../logs/scene-cd32-cd32-s7-n1024.jsonl) · [Protocol](../../preregistration.md)
