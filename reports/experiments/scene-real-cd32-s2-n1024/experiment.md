# scene-real-cd32-s2-n1024

scene / real / cd32 / 1024 families. Seed 2, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 3. Validation accuracy was 53.91% and test accuracy was 49.07%. Both mates were correct in 15.92% of families. The oracle scored 93.51%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-real-cd32-s2-n1024 | 11737 | 53.91% | 49.07% | 15.92% | 51.56% | 50.59% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 17.8 epoch-loop seconds. Peak allocated device memory was 38,983,680 bytes. Source revision 208481e3a01e9925d90955dd1beef5421d52ae3e.

[Manifest](../../../results/scene-real-cd32-s2-n1024/train.json) · [Epoch log](../../../logs/scene-real-cd32-s2-n1024.jsonl) · [Protocol](../../preregistration.md)
