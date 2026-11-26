# scene-cd32-cd32-s42-n1024

scene / cd32 / cd32 / 1024 families. Seed 42, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 35. Validation accuracy was 91.60% and test accuracy was 89.16%. Both mates were correct in 82.23% of families. The oracle scored 93.55%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-cd32-cd32-s42-n1024 | 3801 | 91.60% | 89.16% | 82.23% | 89.79% | 88.82% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 33.0 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision 20d073ba492ae3eec9f16904050f5f1cb7047b73.

[Manifest](../../../results/scene-cd32-cd32-s42-n1024/train.json) · [Epoch log](../../../logs/scene-cd32-cd32-s42-n1024.jsonl) · [Protocol](../../preregistration.md)
