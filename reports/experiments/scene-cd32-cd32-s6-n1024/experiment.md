# scene-cd32-cd32-s6-n1024

scene / cd32 / cd32 / 1024 families. Seed 6, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 55. Validation accuracy was 89.65% and test accuracy was 90.33%. Both mates were correct in 83.98% of families. The oracle scored 94.14%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-cd32-cd32-s6-n1024 | 3801 | 89.65% | 90.33% | 83.98% | 89.99% | 88.57% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 28.4 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision 1c4466404b01970316ffcd26ead8a216f58e87fe.

[Manifest](../../../results/scene-cd32-cd32-s6-n1024/train.json) · [Epoch log](../../../logs/scene-cd32-cd32-s6-n1024.jsonl) · [Protocol](../../preregistration.md)
