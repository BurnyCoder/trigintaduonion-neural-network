# scene-frozen-cd32-s4-n1024

scene / frozen / cd32 / 1024 families. Seed 4, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 5. Validation accuracy was 50.39% and test accuracy was 50.15%. Both mates were correct in 11.23% of families. The oracle scored 93.16%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-frozen-cd32-s4-n1024 | 2113 | 50.39% | 50.15% | 11.23% | 50.49% | 50.98% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 15.9 epoch-loop seconds. Peak allocated device memory was 37,708,800 bytes. Source revision 68a9f4d66b04c620d8350c57bea63851c2390477.

[Manifest](../../../results/scene-frozen-cd32-s4-n1024/train.json) · [Epoch log](../../../logs/scene-frozen-cd32-s4-n1024.jsonl) · [Protocol](../../preregistration.md)
