# Experiment index

The pilot classified 89.16% of 2,048 unseen scenes correctly and answered both mates correctly in 82.23% of families. The constant control scored 50.00% and the privileged sensor-and-geometry oracle scored 93.55%. On unseen sensor coordinates accuracy was 89.79%. Seed 42 is excluded from all confirmatory contrasts. The registered crossover awaits complete paired worlds.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| [scene-cd32-cd32-s42-n1024](scene-cd32-cd32-s42-n1024/experiment.md) | 3801 | 91.60% | 89.16% | 82.23% | 89.79% | 88.82% |

The scene objective is binary cross entropy. The pixel and superpixel objectives are ten-way cross entropy. Each optimizer follows a cosine schedule. The run matrix records the budgets and split choices. Both mates measures the fraction of scene families for which both binary decisions are correct. NMSE divides squared error by total target energy.

[Design and optimizer choices](../planned-runs.md) · [Model details](../../docs/usage.md)

## Independent algebra diagnostics

| Diagnostic | Teacher | Learner | Examples | Seeds | Mean NMSE | Correct basis products |
| --- | --- | --- | --- | --- | --- | --- |
| multiplier | cd32 | cd32 | 2 | 3 | 3.57e-31 | — |
| multiplier | cd32 | random | 2 | 3 | 1.77 | — |
| multiplier | cd32 | real | 2 | 3 | 0.933 | — |
| multiplier | cd32 | cd32 | 8 | 3 | 2.57e-31 | — |
| multiplier | cd32 | random | 8 | 3 | 0.943 | — |
| multiplier | cd32 | real | 8 | 3 | 0.733 | — |
| multiplier | cd32 | cd32 | 32 | 3 | 2.61e-31 | — |
| multiplier | cd32 | random | 32 | 3 | 0.847 | — |
| multiplier | cd32 | real | 32 | 3 | 1.97e-28 | — |
| multiplier | cd32 | cd32 | 128 | 3 | 3.73e-31 | — |
| multiplier | cd32 | random | 128 | 3 | 0.825 | — |
| multiplier | cd32 | real | 128 | 3 | 2.32e-31 | — |
| multiplier | random | cd32 | 2 | 3 | 1.52 | — |
| multiplier | random | random | 2 | 3 | 3.3e-31 | — |
| multiplier | random | real | 2 | 3 | 0.937 | — |
| multiplier | random | cd32 | 8 | 3 | 0.938 | — |
| multiplier | random | random | 8 | 3 | 2.37e-31 | — |
| multiplier | random | real | 8 | 3 | 0.74 | — |
| multiplier | random | cd32 | 32 | 3 | 0.843 | — |
| multiplier | random | random | 32 | 3 | 2.67e-31 | — |
| multiplier | random | real | 32 | 3 | 1.71e-28 | — |
| multiplier | random | cd32 | 128 | 3 | 0.822 | — |
| multiplier | random | random | 128 | 3 | 3.11e-31 | — |
| multiplier | random | real | 128 | 3 | 2.34e-31 | — |
| product | cd32 | bilinear | 256 | 3 | 0.742 | 826.0 |
| product | cd32 | shuffled | 256 | 3 | 1.38 | 17.3 |
| product | cd32 | bilinear | 1024 | 3 | 4.69e-27 | 1024.0 |
| product | cd32 | shuffled | 1024 | 3 | 3.84e+03 | 15.0 |
| product | cd32 | bilinear | 2048 | 3 | 1.95e-30 | 1024.0 |
| product | cd32 | shuffled | 2048 | 3 | 2.07 | 16.0 |
| product | cd32 | analytic | 0 | 3 | 0 | 1024.0 |
