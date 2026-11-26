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
| multiplier | cd32 | cd32 | 2 | 5 | 3.79e-31 | — |
| multiplier | cd32 | random | 2 | 5 | 1.65 | — |
| multiplier | cd32 | real | 2 | 5 | 0.933 | — |
| multiplier | cd32 | cd32 | 8 | 5 | 2.43e-31 | — |
| multiplier | cd32 | random | 8 | 5 | 0.967 | — |
| multiplier | cd32 | real | 8 | 5 | 0.732 | — |
| multiplier | cd32 | cd32 | 32 | 5 | 2.74e-31 | — |
| multiplier | cd32 | random | 32 | 5 | 0.858 | — |
| multiplier | cd32 | real | 32 | 5 | 1.31e-28 | — |
| multiplier | cd32 | cd32 | 128 | 5 | 3.78e-31 | — |
| multiplier | cd32 | random | 128 | 5 | 0.836 | — |
| multiplier | cd32 | real | 128 | 5 | 2.49e-31 | — |
| multiplier | random | cd32 | 2 | 5 | 1.69 | — |
| multiplier | random | random | 2 | 5 | 3.86e-31 | — |
| multiplier | random | real | 2 | 5 | 0.929 | — |
| multiplier | random | cd32 | 8 | 5 | 0.942 | — |
| multiplier | random | random | 8 | 5 | 2.12e-31 | — |
| multiplier | random | real | 8 | 5 | 0.736 | — |
| multiplier | random | cd32 | 32 | 5 | 0.855 | — |
| multiplier | random | random | 32 | 5 | 2.49e-31 | — |
| multiplier | random | real | 32 | 5 | 1.26e-28 | — |
| multiplier | random | cd32 | 128 | 5 | 0.835 | — |
| multiplier | random | random | 128 | 5 | 3.3e-31 | — |
| multiplier | random | real | 128 | 5 | 2.44e-31 | — |
| product | cd32 | bilinear | 256 | 5 | 0.744 | 829.0 |
| product | cd32 | shuffled | 256 | 5 | 1.38 | 17.8 |
| product | cd32 | bilinear | 1024 | 5 | 5.28e-27 | 1024.0 |
| product | cd32 | shuffled | 1024 | 5 | 3.79e+03 | 14.6 |
| product | cd32 | bilinear | 2048 | 5 | 1.94e-30 | 1024.0 |
| product | cd32 | shuffled | 2048 | 5 | 2.06 | 18.0 |
| product | cd32 | analytic | 0 | 5 | 0 | 1024.0 |
