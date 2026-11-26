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
| multiplier | cd32 | cd32 | 2 | 7 | 3.29e-31 | — |
| multiplier | cd32 | random | 2 | 7 | 1.66 | — |
| multiplier | cd32 | real | 2 | 7 | 0.935 | — |
| multiplier | cd32 | cd32 | 8 | 7 | 2.37e-31 | — |
| multiplier | cd32 | random | 8 | 7 | 0.952 | — |
| multiplier | cd32 | real | 8 | 7 | 0.733 | — |
| multiplier | cd32 | cd32 | 32 | 7 | 2.87e-31 | — |
| multiplier | cd32 | random | 32 | 7 | 0.852 | — |
| multiplier | cd32 | real | 32 | 7 | 9.57e-29 | — |
| multiplier | cd32 | cd32 | 128 | 7 | 3.73e-31 | — |
| multiplier | cd32 | random | 128 | 7 | 0.831 | — |
| multiplier | cd32 | real | 128 | 7 | 2.53e-31 | — |
| multiplier | random | cd32 | 2 | 7 | 1.62 | — |
| multiplier | random | random | 2 | 7 | 3.56e-31 | — |
| multiplier | random | real | 2 | 7 | 0.928 | — |
| multiplier | random | cd32 | 8 | 7 | 0.932 | — |
| multiplier | random | random | 8 | 7 | 2.05e-31 | — |
| multiplier | random | real | 8 | 7 | 0.735 | — |
| multiplier | random | cd32 | 32 | 7 | 0.851 | — |
| multiplier | random | random | 32 | 7 | 2.48e-31 | — |
| multiplier | random | real | 32 | 7 | 9.17e-29 | — |
| multiplier | random | cd32 | 128 | 7 | 0.83 | — |
| multiplier | random | random | 128 | 7 | 3.27e-31 | — |
| multiplier | random | real | 128 | 7 | 2.52e-31 | — |
| product | cd32 | bilinear | 256 | 7 | 0.745 | 830.9 |
| product | cd32 | shuffled | 256 | 7 | 1.37 | 18.0 |
| product | cd32 | bilinear | 1024 | 7 | 3.14e-26 | 1024.0 |
| product | cd32 | shuffled | 1024 | 7 | 1.8e+04 | 15.9 |
| product | cd32 | bilinear | 2048 | 7 | 1.95e-30 | 1024.0 |
| product | cd32 | shuffled | 2048 | 7 | 2.07 | 17.1 |
| product | cd32 | analytic | 0 | 7 | 0 | 1024.0 |
