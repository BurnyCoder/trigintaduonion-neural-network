# scene-shallow-cd32-s0-n1024

scene / shallow / cd32 / 1024 families. Seed 0, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 23. Validation accuracy was 50.39% and test accuracy was 50.00%. Both mates were correct in 0.10% of families. The oracle scored 93.95%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-shallow-cd32-s0-n1024 | 7713 | 50.39% | 50.00% | 0.10% | 50.00% | 50.00% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 9.3 epoch-loop seconds. Peak allocated device memory was 39,115,776 bytes. Source revision 34b0ca30242718291934fe1c64efd009c50e4e29.

[Manifest](../../../results/scene-shallow-cd32-s0-n1024/train.json) · [Epoch log](../../../logs/scene-shallow-cd32-s0-n1024.jsonl) · [Protocol](../../preregistration.md)
