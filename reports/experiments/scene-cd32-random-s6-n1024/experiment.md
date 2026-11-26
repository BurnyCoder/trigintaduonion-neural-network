# scene-cd32-random-s6-n1024

scene / cd32 / random / 1024 families. Seed 6, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 6. Validation accuracy was 56.64% and test accuracy was 51.90%. Both mates were correct in 21.48% of families. The oracle scored 92.92%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-cd32-random-s6-n1024 | 3801 | 56.64% | 51.90% | 21.48% | 51.95% | 50.15% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 24.3 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision 692278eeaae3e632a9f3bc0c7782f9dfb28483f4.

[Manifest](../../../results/scene-cd32-random-s6-n1024/train.json) · [Epoch log](../../../logs/scene-cd32-random-s6-n1024.jsonl) · [Protocol](../../preregistration.md)
