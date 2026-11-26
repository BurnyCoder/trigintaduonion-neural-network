# scene-cd16-cd32-s1-n1024

scene / cd16 / cd32 / 1024 families. Seed 1, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 48. Validation accuracy was 66.41% and test accuracy was 66.26%. Both mates were correct in 44.34% of families. The oracle scored 93.41%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-cd16-cd32-s1-n1024 | 4057 | 66.41% | 66.26% | 44.34% | 65.67% | 66.31% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 20.5 epoch-loop seconds. Peak allocated device memory was 38,923,776 bytes. Source revision 940767ab5d2464d7fd4ca4a1e33d0bffb544b339.

[Manifest](../../../results/scene-cd16-cd32-s1-n1024/train.json) · [Epoch log](../../../logs/scene-cd16-cd32-s1-n1024.jsonl) · [Protocol](../../preregistration.md)
