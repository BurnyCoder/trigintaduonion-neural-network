# scene-frozen-cd32-s5-n1024

scene / frozen / cd32 / 1024 families. Seed 5, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 59. Validation accuracy was 51.56% and test accuracy was 51.46%. Both mates were correct in 19.73% of families. The oracle scored 94.73%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-frozen-cd32-s5-n1024 | 2113 | 51.56% | 51.46% | 19.73% | 49.17% | 50.88% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 15.4 epoch-loop seconds. Peak allocated device memory was 37,708,800 bytes. Source revision 3c4a7f83b6f7c74ba9f8e49b80844da46313e5ed.

[Manifest](../../../results/scene-frozen-cd32-s5-n1024/train.json) · [Epoch log](../../../logs/scene-frozen-cd32-s5-n1024.jsonl) · [Protocol](../../preregistration.md)
