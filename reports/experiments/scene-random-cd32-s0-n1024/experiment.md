# scene-random-cd32-s0-n1024

scene / random / cd32 / 1024 families. Seed 0, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 11. Validation accuracy was 53.12% and test accuracy was 51.42%. Both mates were correct in 23.14% of families. The oracle scored 93.95%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-random-cd32-s0-n1024 | 3801 | 53.12% | 51.42% | 23.14% | 51.81% | 48.68% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 31.3 epoch-loop seconds. Peak allocated device memory was 39,038,464 bytes. Source revision 58b8d508d566df26cb3655f897644988ff3eec5c.

[Manifest](../../../results/scene-random-cd32-s0-n1024/train.json) · [Epoch log](../../../logs/scene-random-cd32-s0-n1024.jsonl) · [Protocol](../../preregistration.md)
