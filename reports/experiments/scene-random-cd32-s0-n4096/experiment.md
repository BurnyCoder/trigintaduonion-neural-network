# scene-random-cd32-s0-n4096

scene / random / cd32 / 4096 families. Seed 0, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 59. Validation accuracy was 55.66% and test accuracy was 50.88%. Both mates were correct in 25.10% of families. The oracle scored 93.95%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-random-cd32-s0-n4096 | 3801 | 55.66% | 50.88% | 25.10% | 50.10% | 48.97% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 86.6 epoch-loop seconds. Peak allocated device memory was 46,598,656 bytes. Source revision d057e5032f7f359b8061405b507521555e4efaef.

[Manifest](../../../results/scene-random-cd32-s0-n4096/train.json) · [Epoch log](../../../logs/scene-random-cd32-s0-n4096.jsonl) · [Protocol](../../preregistration.md)
