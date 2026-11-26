# scene-random-cd32-s6-n1024

scene / random / cd32 / 1024 families. Seed 6, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 5. Validation accuracy was 51.95% and test accuracy was 51.22%. Both mates were correct in 20.90% of families. The oracle scored 94.14%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-random-cd32-s6-n1024 | 3801 | 51.95% | 51.22% | 20.90% | 50.83% | 49.32% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 24.1 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision b2a5e797b3b1bc11716ec95c3e40047671501ffe.

[Manifest](../../../results/scene-random-cd32-s6-n1024/train.json) · [Epoch log](../../../logs/scene-random-cd32-s6-n1024.jsonl) · [Protocol](../../preregistration.md)
