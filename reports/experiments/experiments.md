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
| multiplier | cd32 | cd32 | 2 | 2 | 3.46e-31 | — |
| multiplier | cd32 | random | 2 | 2 | 1.76 | — |
| multiplier | cd32 | real | 2 | 2 | 0.937 | — |
| multiplier | cd32 | cd32 | 8 | 2 | 2.87e-31 | — |
| multiplier | cd32 | random | 8 | 2 | 0.947 | — |
| multiplier | cd32 | real | 8 | 2 | 0.739 | — |
| multiplier | cd32 | cd32 | 32 | 2 | 2.36e-31 | — |
| multiplier | cd32 | random | 32 | 2 | 0.881 | — |
| multiplier | cd32 | real | 32 | 2 | 8.85e-29 | — |
| multiplier | cd32 | cd32 | 128 | 2 | 3.1e-31 | — |
| multiplier | cd32 | random | 128 | 2 | 0.858 | — |
| multiplier | cd32 | real | 128 | 2 | 2.31e-31 | — |
| multiplier | random | cd32 | 2 | 2 | 1.54 | — |
| multiplier | random | random | 2 | 2 | 3.19e-31 | — |
| multiplier | random | real | 2 | 2 | 0.94 | — |
| multiplier | random | cd32 | 8 | 2 | 0.933 | — |
| multiplier | random | random | 8 | 2 | 1.98e-31 | — |
| multiplier | random | real | 8 | 2 | 0.742 | — |
| multiplier | random | cd32 | 32 | 2 | 0.878 | — |
| multiplier | random | random | 32 | 2 | 3.34e-31 | — |
| multiplier | random | real | 32 | 2 | 1.18e-28 | — |
| multiplier | random | cd32 | 128 | 2 | 0.853 | — |
| multiplier | random | random | 128 | 2 | 3.23e-31 | — |
| multiplier | random | real | 128 | 2 | 2.34e-31 | — |
| product | cd32 | bilinear | 256 | 2 | 0.746 | 829.0 |
| product | cd32 | shuffled | 256 | 2 | 1.38 | 21.0 |
| product | cd32 | bilinear | 1024 | 2 | 4.13e-27 | 1024.0 |
| product | cd32 | shuffled | 1024 | 2 | 3.68e+03 | 16.0 |
| product | cd32 | bilinear | 2048 | 2 | 1.96e-30 | 1024.0 |
| product | cd32 | shuffled | 2048 | 2 | 2.07 | 16.5 |
| product | cd32 | analytic | 0 | 2 | 0 | 1024.0 |
