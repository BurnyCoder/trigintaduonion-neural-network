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
