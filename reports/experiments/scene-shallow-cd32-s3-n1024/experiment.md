# scene-shallow-cd32-s3-n1024

scene / shallow / cd32 / 1024 families. Seed 3, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 43. Validation accuracy was 50.39% and test accuracy was 49.85%. Both mates were correct in 0.00% of families. The oracle scored 93.65%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-shallow-cd32-s3-n1024 | 7713 | 50.39% | 49.85% | 0.00% | 50.10% | 50.00% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 7.6 epoch-loop seconds. Peak allocated device memory was 39,115,776 bytes. Source revision 730d9c8025517db1a6db5073fb49a6485ed106ce.

[Manifest](../../../results/scene-shallow-cd32-s3-n1024/train.json) · [Epoch log](../../../logs/scene-shallow-cd32-s3-n1024.jsonl) · [Protocol](../../preregistration.md)
