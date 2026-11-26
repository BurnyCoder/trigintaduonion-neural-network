# scene-frozen-cd32-s2-n1024

scene / frozen / cd32 / 1024 families. Seed 2, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 35. Validation accuracy was 54.10% and test accuracy was 50.73%. Both mates were correct in 18.46% of families. The oracle scored 93.51%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-frozen-cd32-s2-n1024 | 2113 | 54.10% | 50.73% | 18.46% | 50.29% | 51.76% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 16.5 epoch-loop seconds. Peak allocated device memory was 37,708,800 bytes. Source revision 21c1a8cf33e3f6c285dbe6bf64749574f9649235.

[Manifest](../../../results/scene-frozen-cd32-s2-n1024/train.json) · [Epoch log](../../../logs/scene-frozen-cd32-s2-n1024.jsonl) · [Protocol](../../preregistration.md)
