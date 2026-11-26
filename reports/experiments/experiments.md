# Experiment index

The pilot classified 89.16% of 2,048 unseen scenes correctly and answered both mates correctly in 82.23% of families. The constant control scored 50.00% and the privileged sensor-and-geometry oracle scored 93.55%. On unseen sensor coordinates accuracy was 89.79%. Seed 42 is excluded from all confirmatory contrasts. The registered crossover awaits complete paired worlds.

| Run | Trainable | Validation | Test | Both mates | Held-out channels | Crowded / ciFAIR |
| --- | --- | --- | --- | --- | --- | --- |
| [scene-cd32-cd32-s0-n1024](scene-cd32-cd32-s0-n1024/experiment.md) | 3801 | 91.99% | pending | pending | pending | pending |
| [scene-cd32-cd32-s1-n1024](scene-cd32-cd32-s1-n1024/experiment.md) | 3801 | 90.43% | pending | pending | pending | pending |
| [scene-cd32-cd32-s42-n1024](scene-cd32-cd32-s42-n1024/experiment.md) | 3801 | 91.60% | 89.16% | 82.23% | 89.79% | 88.82% |
| [scene-cd32-random-s0-n1024](scene-cd32-random-s0-n1024/experiment.md) | 3801 | 53.91% | pending | pending | pending | pending |
| [scene-random-cd32-s0-n1024](scene-random-cd32-s0-n1024/experiment.md) | 3801 | 53.12% | pending | pending | pending | pending |
| [scene-random-cd32-s1-n1024](scene-random-cd32-s1-n1024/experiment.md) | 3801 | 56.84% | pending | pending | pending | pending |
| [scene-random-random-s0-n1024](scene-random-random-s0-n1024/experiment.md) | 3801 | 89.84% | pending | pending | pending | pending |

The scene objective is binary cross entropy. The pixel and superpixel objectives are ten-way cross entropy. Each optimizer follows a cosine schedule. The run matrix records the budgets and split choices. Both mates measures the fraction of scene families for which both binary decisions are correct. NMSE divides squared error by total target energy.

[Design and optimizer choices](../planned-runs.md) · [Model details](../../docs/usage.md)

## Independent algebra diagnostics

| Diagnostic | Teacher | Learner | Examples | Seeds | Mean NMSE | Correct basis products |
| --- | --- | --- | --- | --- | --- | --- |
| multiplier | cd32 | cd32 | 2 | 8 | 3.32e-31 | — |
| multiplier | cd32 | random | 2 | 8 | 1.63 | — |
| multiplier | cd32 | real | 2 | 8 | 0.936 | — |
| multiplier | cd32 | cd32 | 8 | 8 | 2.35e-31 | — |
| multiplier | cd32 | random | 8 | 8 | 0.962 | — |
| multiplier | cd32 | real | 8 | 8 | 0.737 | — |
| multiplier | cd32 | cd32 | 32 | 8 | 2.88e-31 | — |
| multiplier | cd32 | random | 32 | 8 | 0.86 | — |
| multiplier | cd32 | real | 32 | 8 | 1.93e-28 | — |
| multiplier | cd32 | cd32 | 128 | 8 | 3.6e-31 | — |
| multiplier | cd32 | random | 128 | 8 | 0.838 | — |
| multiplier | cd32 | real | 128 | 8 | 2.5e-31 | — |
| multiplier | random | cd32 | 2 | 8 | 1.57 | — |
| multiplier | random | random | 2 | 8 | 3.45e-31 | — |
| multiplier | random | real | 2 | 8 | 0.929 | — |
| multiplier | random | cd32 | 8 | 8 | 0.943 | — |
| multiplier | random | random | 8 | 8 | 2e-31 | — |
| multiplier | random | real | 8 | 8 | 0.741 | — |
| multiplier | random | cd32 | 32 | 8 | 0.856 | — |
| multiplier | random | random | 32 | 8 | 2.48e-31 | — |
| multiplier | random | real | 32 | 8 | 3.44e-28 | — |
| multiplier | random | cd32 | 128 | 8 | 0.835 | — |
| multiplier | random | random | 128 | 8 | 3.7e-31 | — |
| multiplier | random | real | 128 | 8 | 2.49e-31 | — |
| product | cd32 | bilinear | 256 | 8 | 0.745 | 830.0 |
| product | cd32 | shuffled | 256 | 8 | 1.38 | 17.8 |
| product | cd32 | bilinear | 1024 | 8 | 2.78e-26 | 1024.0 |
| product | cd32 | shuffled | 1024 | 8 | 1.6e+04 | 15.2 |
| product | cd32 | bilinear | 2048 | 8 | 1.94e-30 | 1024.0 |
| product | cd32 | shuffled | 2048 | 8 | 2.06 | 17.8 |
| product | cd32 | analytic | 0 | 8 | 0 | 1024.0 |
