# scene-random-cd32-s0-n32768

scene / random / cd32 / 32768 families. Seed 0, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 66. Validation accuracy was 56.64% and test accuracy was 54.93%. Both mates were correct in 28.91% of families. The oracle scored 93.95%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-random-cd32-s0-n32768 | 3801 | 56.64% | 54.93% | 28.91% | 54.44% | 53.81% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 736.9 epoch-loop seconds. Peak allocated device memory was 117,934,592 bytes. Source revision 8a381b1a560f03e2ee2201e3e1fce5e3c06ca999.

[Manifest](../../../results/scene-random-cd32-s0-n32768/train.json) · [Epoch log](../../../logs/scene-random-cd32-s0-n32768.jsonl) · [Protocol](../../preregistration.md)
