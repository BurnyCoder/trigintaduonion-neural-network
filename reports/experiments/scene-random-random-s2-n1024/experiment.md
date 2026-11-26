# scene-random-random-s2-n1024

scene / random / random / 1024 families. Seed 2, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 40. Validation accuracy was 91.41% and test accuracy was 90.38%. Both mates were correct in 84.18% of families. The oracle scored 93.80%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-random-random-s2-n1024 | 3801 | 91.41% | 90.38% | 84.18% | 90.67% | 89.01% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 28.1 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision 6ca33f657d63e13c35e81508df900a838347ac9d.

[Manifest](../../../results/scene-random-random-s2-n1024/train.json) · [Epoch log](../../../logs/scene-random-random-s2-n1024.jsonl) · [Protocol](../../preregistration.md)
