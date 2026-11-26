# scene-random-random-s3-n1024

scene / random / random / 1024 families. Seed 3, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 36. Validation accuracy was 91.41% and test accuracy was 89.16%. Both mates were correct in 83.11% of families. The oracle scored 93.36%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-random-random-s3-n1024 | 3801 | 91.41% | 89.16% | 83.11% | 88.87% | 87.89% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 22.8 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision 92c2e76b56acc20643693834674f2e84ec0d4087.

[Manifest](../../../results/scene-random-random-s3-n1024/train.json) · [Epoch log](../../../logs/scene-random-random-s3-n1024.jsonl) · [Protocol](../../preregistration.md)
