# scene-random-random-s5-n1024

scene / random / random / 1024 families. Seed 5, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 45. Validation accuracy was 92.38% and test accuracy was 90.58%. Both mates were correct in 84.67% of families. The oracle scored 94.97%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-random-random-s5-n1024 | 3801 | 92.38% | 90.58% | 84.67% | 90.43% | 89.60% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 26.5 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision 83af83f84cd0d4301e7b14be2035d5e2837d212d.

[Manifest](../../../results/scene-random-random-s5-n1024/train.json) · [Epoch log](../../../logs/scene-random-random-s5-n1024.jsonl) · [Protocol](../../preregistration.md)
