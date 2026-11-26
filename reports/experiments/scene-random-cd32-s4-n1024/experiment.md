# scene-random-cd32-s4-n1024

scene / random / cd32 / 1024 families. Seed 4, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 1. Validation accuracy was 51.37% and test accuracy was 50.88%. Both mates were correct in 16.50% of families. The oracle scored 93.16%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-random-cd32-s4-n1024 | 3801 | 51.37% | 50.88% | 16.50% | 49.56% | 48.88% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 24.5 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision 924b72020d6b9861a950db64908dd8b61850cd99.

[Manifest](../../../results/scene-random-cd32-s4-n1024/train.json) · [Epoch log](../../../logs/scene-random-cd32-s4-n1024.jsonl) · [Protocol](../../preregistration.md)
