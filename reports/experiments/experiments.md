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
| multiplier | cd32 | cd32 | 2 | 1 | 2.47e-31 | — |
| multiplier | cd32 | random | 2 | 1 | 1.79 | — |
| multiplier | cd32 | real | 2 | 1 | 0.935 | — |
| multiplier | cd32 | cd32 | 8 | 1 | 3.82e-31 | — |
| multiplier | cd32 | random | 8 | 1 | 0.907 | — |
| multiplier | cd32 | real | 8 | 1 | 0.727 | — |
| multiplier | cd32 | cd32 | 32 | 1 | 2.76e-31 | — |
| multiplier | cd32 | random | 32 | 1 | 0.851 | — |
| multiplier | cd32 | real | 32 | 1 | 1.64e-29 | — |
| multiplier | cd32 | cd32 | 128 | 1 | 3.1e-31 | — |
| multiplier | cd32 | random | 128 | 1 | 0.827 | — |
| multiplier | cd32 | real | 128 | 1 | 2.31e-31 | — |
| multiplier | random | cd32 | 2 | 1 | 1.58 | — |
| multiplier | random | random | 2 | 1 | 3.64e-31 | — |
| multiplier | random | real | 2 | 1 | 0.927 | — |
| multiplier | random | cd32 | 8 | 1 | 0.903 | — |
| multiplier | random | random | 8 | 1 | 1.95e-31 | — |
| multiplier | random | real | 8 | 1 | 0.736 | — |
| multiplier | random | cd32 | 32 | 1 | 0.846 | — |
| multiplier | random | random | 32 | 1 | 1.78e-31 | — |
| multiplier | random | real | 32 | 1 | 1.52e-29 | — |
| multiplier | random | cd32 | 128 | 1 | 0.82 | — |
| multiplier | random | random | 128 | 1 | 3.4e-31 | — |
| multiplier | random | real | 128 | 1 | 2.38e-31 | — |
| product | cd32 | bilinear | 256 | 1 | 0.749 | 839.0 |
| product | cd32 | shuffled | 256 | 1 | 1.38 | 23.0 |
| product | cd32 | bilinear | 1024 | 1 | 3.55e-27 | 1024.0 |
| product | cd32 | shuffled | 1024 | 1 | 2.97e+03 | 18.0 |
| product | cd32 | bilinear | 2048 | 1 | 1.93e-30 | 1024.0 |
| product | cd32 | shuffled | 2048 | 1 | 2.09 | 14.0 |
| product | cd32 | analytic | 0 | 1 | 0 | 1024.0 |
