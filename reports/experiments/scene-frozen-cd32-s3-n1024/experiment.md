# scene-frozen-cd32-s3-n1024

scene / frozen / cd32 / 1024 families. Seed 3, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 10. Validation accuracy was 52.93% and test accuracy was 49.80%. Both mates were correct in 13.18% of families. The oracle scored 93.65%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-frozen-cd32-s3-n1024 | 2113 | 52.93% | 49.80% | 13.18% | 49.22% | 49.41% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 15.7 epoch-loop seconds. Peak allocated device memory was 37,708,800 bytes. Source revision 374750e546864ddc7e93685128bb703ae9c7939e.

[Manifest](../../../results/scene-frozen-cd32-s3-n1024/train.json) · [Epoch log](../../../logs/scene-frozen-cd32-s3-n1024.jsonl) · [Protocol](../../preregistration.md)
