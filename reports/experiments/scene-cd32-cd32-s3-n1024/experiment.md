# scene-cd32-cd32-s3-n1024

scene / cd32 / cd32 / 1024 families. Seed 3, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 34. Validation accuracy was 88.28% and test accuracy was 89.21%. Both mates were correct in 81.84% of families. The oracle scored 93.65%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-cd32-cd32-s3-n1024 | 3801 | 88.28% | 89.21% | 81.84% | 88.57% | 86.08% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 25.1 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision cdd32a79acb0373fcd69eec858a9fb2ba4b6291e.

[Manifest](../../../results/scene-cd32-cd32-s3-n1024/train.json) · [Epoch log](../../../logs/scene-cd32-cd32-s3-n1024.jsonl) · [Protocol](../../preregistration.md)
