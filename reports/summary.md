# Results

The pilot classified 89.16% of 2,048 unseen scenes correctly and answered both mates correctly in 82.23% of families. The constant control scored 50.00% and the privileged sensor-and-geometry oracle scored 93.55%. On unseen sensor coordinates accuracy was 89.79%. Seed 42 is excluded from all confirmatory contrasts. The registered crossover awaits complete paired worlds.

| Task / learner / sensor | Tested worlds | Trainable | Mean test | 95% interval |
| --- | --- | --- | --- | --- |
| scene / budget / cd32 / 1024 families | 0 | 3961 | pending | — |
| scene / cd16 / cd32 / 1024 families | 0 | 4057 | pending | — |
| scene / cd32 / cd32 / 1024 families | 4 | 3801 | 90.01% | 88.46% to 91.57% |
| scene / cd32 / cd32 / 1024 families (pilot) | 1 | 3801 | 89.16% | — |
| scene / cd32 / random / 1024 families | 4 | 3801 | 50.59% | 49.76% to 51.41% |
| scene / frozen / cd32 / 1024 families | 0 | 2113 | pending | — |
| scene / onehop / cd32 / 1024 families | 0 | 3801 | pending | — |
| scene / random / cd32 / 1024 families | 4 | 3801 | 50.26% | 48.58% to 51.94% |
| scene / random / random / 1024 families | 4 | 3801 | 90.01% | 89.04% to 90.99% |
| scene / real / cd32 / 1024 families | 0 | 11737 | pending | — |
| scene / shallow / cd32 / 1024 families | 0 | 7713 | pending | — |

| Registered endpoint | Worlds | Estimate | 95% interval | Threshold | Decision |
| --- | --- | --- | --- | --- | --- |
| Matched canonical accuracy | 4 | 90.01% | 88.46% to 91.57% | 60.00% | pending |
| Matched randomized accuracy | 4 | 90.01% | 89.04% to 90.99% | 60.00% | pending |
| Canonical minus randomized on canonical sensors | 4 | 39.76 pp | 37.55 pp to 41.96 pp | 1.00 pp | pending |
| Randomized minus canonical on randomized sensors | 4 | 39.43 pp | 38.22 pp to 40.63 pp | 1.00 pp | pending |
| Canonical minus frozen | 0 | pending | — | 0.00 pp | pending |
| Canonical minus validation-selected shallow control | 0 | pending | — | 0.00 pp | pending |
| Canonical minus randomized on ciFAIR-10 | 0 | pending | — | 1.00 pp | pending |

## Counterfactual families and distribution shifts

| Learner | Sensor | Worlds | Test | Both mates | Unseen channels | Crowded | Constant | Known-filter oracle |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cd32 | cd32 | 4 | 90.01% | 83.47% | 89.32% | 88.28% | 50.00% | 93.63% |
| cd32 | random | 4 | 50.59% | 24.10% | 50.83% | 49.96% | 50.00% | 93.65% |
| random | cd32 | 4 | 50.26% | 21.80% | 50.27% | 49.46% | 50.00% | 93.63% |
| random | random | 4 | 90.01% | 83.86% | 90.01% | 88.93% | 50.00% | 93.65% |

Each entry averages the saved world-level scores. Both mates counts families whose two opposite labels were both predicted correctly. The last two columns evaluate analytic controls on the original test scenes.

## Supplementary fixed-checkpoint interventions

| Run | Input | Accuracy against original labels | Decisions changed | Max Δ probability |
| --- | --- | --- | --- | --- |
| scene-cd32-cd32-s42-n1024 | original | 89.16% | 0 | 0 |
| scene-cd32-cd32-s42-n1024 | isometry_and_reindexing | 89.16% | 0 | 0.0306 |
| scene-cd32-cd32-s42-n1024 | broken_correspondence | 49.85% | 1009 | 1 |

The float64 symmetry reference for scene-cd32-cd32-s42-n1024 changed 0 decisions. Maximum absolute probability drift was 2.61e-14.

Scene intervals use a two-sided Student t across independent worlds. Each image seed evaluates the same images, so the image interval measures training variability conditional on that test set. Differences use percentage points. A single seed has no between-seed interval. The pilot is excluded from all confirmatory contrasts.

[Raw manifests and predictions](../results/) · [Preregistration](preregistration.md) · [Explorer](https://burnycoder.github.io/trigintaduonion-neural-network/)
