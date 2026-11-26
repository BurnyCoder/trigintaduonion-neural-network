# scene-real-cd32-s1-n1024

scene / real / cd32 / 1024 families. Seed 1, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 3. Validation accuracy was 53.32% and test accuracy was 50.63%. Both mates were correct in 17.68% of families. The oracle scored 93.41%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-real-cd32-s1-n1024 | 11737 | 53.32% | 50.63% | 17.68% | 49.85% | 50.49% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 18.0 epoch-loop seconds. Peak allocated device memory was 38,983,680 bytes. Source revision 081714a7078e5b6f38298dbfb10f04c4f6047916.

[Manifest](../../../results/scene-real-cd32-s1-n1024/train.json) · [Epoch log](../../../logs/scene-real-cd32-s1-n1024.jsonl) · [Protocol](../../preregistration.md)
