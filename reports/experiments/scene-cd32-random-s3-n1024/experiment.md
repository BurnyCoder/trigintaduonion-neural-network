# scene-cd32-random-s3-n1024

scene / cd32 / random / 1024 families. Seed 3, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 11. Validation accuracy was 57.23% and test accuracy was 50.29%. Both mates were correct in 24.32% of families. The oracle scored 93.36%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-cd32-random-s3-n1024 | 3801 | 57.23% | 50.29% | 24.32% | 50.63% | 49.80% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 24.1 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision 7a9d38dac12b91984873a49b27949b16c1cbde9e.

[Manifest](../../../results/scene-cd32-random-s3-n1024/train.json) · [Epoch log](../../../logs/scene-cd32-random-s3-n1024.jsonl) · [Protocol](../../preregistration.md)
