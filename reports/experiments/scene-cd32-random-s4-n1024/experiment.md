# scene-cd32-random-s4-n1024

scene / cd32 / random / 1024 families. Seed 4, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 13. Validation accuracy was 51.37% and test accuracy was 49.41%. Both mates were correct in 21.39% of families. The oracle scored 93.51%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-cd32-random-s4-n1024 | 3801 | 51.37% | 49.41% | 21.39% | 50.93% | 49.46% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 24.6 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision 8b766dff68d36b585ec850f5b58755c1a245e708.

[Manifest](../../../results/scene-cd32-random-s4-n1024/train.json) · [Epoch log](../../../logs/scene-cd32-random-s4-n1024.jsonl) · [Protocol](../../preregistration.md)
