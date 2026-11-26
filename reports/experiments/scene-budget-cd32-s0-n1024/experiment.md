# scene-budget-cd32-s0-n1024

scene / budget / cd32 / 1024 families. Seed 0, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 45. Validation accuracy was 53.12% and test accuracy was 49.51%. Both mates were correct in 22.17% of families. The oracle scored 93.95%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-budget-cd32-s0-n1024 | 3961 | 53.12% | 49.51% | 22.17% | 48.88% | 48.58% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 28.7 epoch-loop seconds. Peak allocated device memory was 38,914,048 bytes. Source revision 71f1fd634853435fde450afb3daefc04d81ec134.

[Manifest](../../../results/scene-budget-cd32-s0-n1024/train.json) · [Epoch log](../../../logs/scene-budget-cd32-s0-n1024.jsonl) · [Protocol](../../preregistration.md)
