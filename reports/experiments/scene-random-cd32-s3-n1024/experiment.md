# scene-random-cd32-s3-n1024

scene / random / cd32 / 1024 families. Seed 3, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 3. Validation accuracy was 51.95% and test accuracy was 50.88%. Both mates were correct in 17.97% of families. The oracle scored 93.65%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-random-cd32-s3-n1024 | 3801 | 51.95% | 50.88% | 17.97% | 51.17% | 49.66% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 24.3 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision e3cf415766dd7b711aa76a726819b5faaa4d2bcf.

[Manifest](../../../results/scene-random-cd32-s3-n1024/train.json) · [Epoch log](../../../logs/scene-random-cd32-s3-n1024.jsonl) · [Protocol](../../preregistration.md)
