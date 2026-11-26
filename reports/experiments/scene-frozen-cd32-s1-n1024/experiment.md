# scene-frozen-cd32-s1-n1024

scene / frozen / cd32 / 1024 families. Seed 1, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 39. Validation accuracy was 53.52% and test accuracy was 50.73%. Both mates were correct in 16.21% of families. The oracle scored 93.41%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-frozen-cd32-s1-n1024 | 2113 | 53.52% | 50.73% | 16.21% | 48.73% | 50.63% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 14.4 epoch-loop seconds. Peak allocated device memory was 37,708,800 bytes. Source revision c9f260cbef514a1cd588fc4670823f58d1d0d48a.

[Manifest](../../../results/scene-frozen-cd32-s1-n1024/train.json) · [Epoch log](../../../logs/scene-frozen-cd32-s1-n1024.jsonl) · [Protocol](../../preregistration.md)
