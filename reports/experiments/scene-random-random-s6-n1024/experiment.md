# scene-random-random-s6-n1024

scene / random / random / 1024 families. Seed 6, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 38. Validation accuracy was 91.21% and test accuracy was 90.48%. Both mates were correct in 84.38% of families. The oracle scored 92.92%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-random-random-s6-n1024 | 3801 | 91.21% | 90.48% | 84.38% | 91.55% | 89.84% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 30.9 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision 03287e065fe691ec9254ea55ea7d61002c08dff5.

[Manifest](../../../results/scene-random-random-s6-n1024/train.json) · [Epoch log](../../../logs/scene-random-random-s6-n1024.jsonl) · [Protocol](../../preregistration.md)
