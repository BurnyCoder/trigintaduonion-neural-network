# scene-cd32-cd32-s2-n1024

scene / cd32 / cd32 / 1024 families. Seed 2, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 32. Validation accuracy was 91.21% and test accuracy was 91.06%. Both mates were correct in 85.35% of families. The oracle scored 93.51%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-cd32-cd32-s2-n1024 | 3801 | 91.21% | 91.06% | 85.35% | 89.65% | 89.45% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 23.8 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision 7d0856c27ca8108a3e36df8af2d0a9b5f96adc8d.

[Manifest](../../../results/scene-cd32-cd32-s2-n1024/train.json) · [Epoch log](../../../logs/scene-cd32-cd32-s2-n1024.jsonl) · [Protocol](../../preregistration.md)
