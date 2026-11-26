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
| multiplier | cd32 | cd32 | 2 | 4 | 3.71e-31 | — |
| multiplier | cd32 | random | 2 | 4 | 1.71 | — |
| multiplier | cd32 | real | 2 | 4 | 0.933 | — |
| multiplier | cd32 | cd32 | 8 | 4 | 2.61e-31 | — |
| multiplier | cd32 | random | 8 | 4 | 0.957 | — |
| multiplier | cd32 | real | 8 | 4 | 0.735 | — |
| multiplier | cd32 | cd32 | 32 | 4 | 2.85e-31 | — |
| multiplier | cd32 | random | 32 | 4 | 0.848 | — |
| multiplier | cd32 | real | 32 | 4 | 1.53e-28 | — |
| multiplier | cd32 | cd32 | 128 | 4 | 3.62e-31 | — |
| multiplier | cd32 | random | 128 | 4 | 0.825 | — |
| multiplier | cd32 | real | 128 | 4 | 2.32e-31 | — |
| multiplier | random | cd32 | 2 | 4 | 1.61 | — |
| multiplier | random | random | 2 | 4 | 4.01e-31 | — |
| multiplier | random | real | 2 | 4 | 0.93 | — |
| multiplier | random | cd32 | 8 | 4 | 0.933 | — |
| multiplier | random | random | 8 | 4 | 2.19e-31 | — |
| multiplier | random | real | 8 | 4 | 0.737 | — |
| multiplier | random | cd32 | 32 | 4 | 0.844 | — |
| multiplier | random | random | 32 | 4 | 2.47e-31 | — |
| multiplier | random | real | 32 | 4 | 1.33e-28 | — |
| multiplier | random | cd32 | 128 | 4 | 0.822 | — |
| multiplier | random | random | 128 | 4 | 3.36e-31 | — |
| multiplier | random | real | 128 | 4 | 2.34e-31 | — |
| product | cd32 | bilinear | 256 | 4 | 0.744 | 830.8 |
| product | cd32 | shuffled | 256 | 4 | 1.38 | 17.8 |
| product | cd32 | bilinear | 1024 | 4 | 3.85e-27 | 1024.0 |
| product | cd32 | shuffled | 1024 | 4 | 3.13e+03 | 15.2 |
| product | cd32 | bilinear | 2048 | 4 | 1.94e-30 | 1024.0 |
| product | cd32 | shuffled | 2048 | 4 | 2.07 | 15.5 |
| product | cd32 | analytic | 0 | 4 | 0 | 1024.0 |
