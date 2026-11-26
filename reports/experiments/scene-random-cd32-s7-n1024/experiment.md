# scene-random-cd32-s7-n1024

scene / random / cd32 / 1024 families. Seed 7, 80 epochs, batch size 128, starting learning rate 0.003. A family contains the original scene and a counterfactual with reversed ground truth.

The selected epoch was 12. Validation accuracy was 53.32% and test accuracy was 49.76%. Both mates were correct in 23.73% of families. The oracle scored 93.36%.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| scene-random-cd32-s7-n1024 | 3801 | 53.32% | 49.76% | 23.73% | 48.83% | 51.07% |

Device NVIDIA GeForce RTX 5070 Laptop GPU. Training took 27.0 epoch-loop seconds. Peak allocated device memory was 38,955,520 bytes. Source revision 66e4102ca365e3c03068ae090b1a63dfa95189ce.

[Manifest](../../../results/scene-random-cd32-s7-n1024/train.json) · [Epoch log](../../../logs/scene-random-cd32-s7-n1024.jsonl) · [Protocol](../../preregistration.md)
