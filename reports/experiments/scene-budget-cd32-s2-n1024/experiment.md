# scene-budget-cd32-s2-n1024

scene / budget / cd32 / 1024 families. Seed 2, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 21. Validation accuracy was 53.32% and test accuracy was 49.32%. Both mates were correct in 19.73% of families. The oracle scored 93.51%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-budget-cd32-s2-n1024 | 3961 | 53.32% | 49.32% | 19.73% | 50.49% | 49.66% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 17.7 epoch-loop seconds. Peak allocated device memory was 38,914,048 bytes. Source revision 573dd0983b727b9f6ff41fcb48995da624845852.

[Manifest](../../../results/scene-budget-cd32-s2-n1024/train.json) · [Epoch log](../../../logs/scene-budget-cd32-s2-n1024.jsonl) · [Protocol](../../preregistration.md)
