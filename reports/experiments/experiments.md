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
| multiplier | cd32 | cd32 | 2 | 6 | 3.5e-31 | — |
| multiplier | cd32 | random | 2 | 6 | 1.62 | — |
| multiplier | cd32 | real | 2 | 6 | 0.935 | — |
| multiplier | cd32 | cd32 | 8 | 6 | 2.4e-31 | — |
| multiplier | cd32 | random | 8 | 6 | 0.963 | — |
| multiplier | cd32 | real | 8 | 6 | 0.73 | — |
| multiplier | cd32 | cd32 | 32 | 6 | 2.59e-31 | — |
| multiplier | cd32 | random | 32 | 6 | 0.859 | — |
| multiplier | cd32 | real | 32 | 6 | 1.11e-28 | — |
| multiplier | cd32 | cd32 | 128 | 6 | 3.44e-31 | — |
| multiplier | cd32 | random | 128 | 6 | 0.837 | — |
| multiplier | cd32 | real | 128 | 6 | 2.52e-31 | — |
| multiplier | random | cd32 | 2 | 6 | 1.63 | — |
| multiplier | random | random | 2 | 6 | 3.75e-31 | — |
| multiplier | random | real | 2 | 6 | 0.931 | — |
| multiplier | random | cd32 | 8 | 6 | 0.941 | — |
| multiplier | random | random | 8 | 6 | 2.18e-31 | — |
| multiplier | random | real | 8 | 6 | 0.737 | — |
| multiplier | random | cd32 | 32 | 6 | 0.855 | — |
| multiplier | random | random | 32 | 6 | 2.36e-31 | — |
| multiplier | random | real | 32 | 6 | 1.06e-28 | — |
| multiplier | random | cd32 | 128 | 6 | 0.834 | — |
| multiplier | random | random | 128 | 6 | 3.24e-31 | — |
| multiplier | random | real | 128 | 6 | 2.47e-31 | — |
| product | cd32 | bilinear | 256 | 6 | 0.745 | 830.0 |
| product | cd32 | shuffled | 256 | 6 | 1.38 | 17.7 |
| product | cd32 | bilinear | 1024 | 6 | 3.62e-26 | 1024.0 |
| product | cd32 | shuffled | 1024 | 6 | 2.08e+04 | 15.3 |
| product | cd32 | bilinear | 2048 | 6 | 1.95e-30 | 1024.0 |
| product | cd32 | shuffled | 2048 | 6 | 2.07 | 17.3 |
| product | cd32 | analytic | 0 | 6 | 0 | 1024.0 |
