# Results

The pilot classified 89.16% of 2,048 unseen scenes correctly and answered both mates correctly in 82.23% of families. The constant control scored 50.00% and the privileged sensor-and-geometry oracle scored 93.55%. On unseen sensor coordinates accuracy was 89.79%. Seed 42 is excluded from all confirmatory contrasts. The registered crossover awaits complete paired worlds.

| Task / learner / sensor | Tested worlds | Trainable | Mean test | 95% interval |
| --- | --- | --- | --- | --- |
| scene / budget / cd32 / 1024 families | 0 | 3961 | pending | — |
| scene / cd16 / cd32 / 1024 families | 0 | 4057 | pending | — |
| scene / cd32 / cd32 / 1024 families | 7 | 3801 | 89.97% | 89.09% to 90.85% |
| scene / cd32 / cd32 / 1024 families (pilot) | 1 | 3801 | 89.16% | — |
| scene / cd32 / random / 1024 families | 6 | 3801 | 50.36% | 49.71% to 51.01% |
| scene / frozen / cd32 / 1024 families | 0 | 2113 | pending | — |
| scene / onehop / cd32 / 1024 families | 0 | 3801 | pending | — |
| scene / random / cd32 / 1024 families | 7 | 3801 | 50.54% | 49.76% to 51.32% |
| scene / random / random / 1024 families | 6 | 3801 | 90.06% | 89.47% to 90.64% |
| scene / real / cd32 / 1024 families | 0 | 11737 | pending | — |
| scene / shallow / cd32 / 1024 families | 0 | 7713 | pending | — |

| Registered endpoint | Worlds | Estimate | 95% interval | Threshold | Decision |
| --- | --- | --- | --- | --- | --- |
| Matched canonical accuracy | 7 | 89.97% | 89.09% to 90.85% | 60.00% | pending |
| Matched randomized accuracy | 6 | 90.06% | 89.47% to 90.64% | 60.00% | pending |
| Canonical minus randomized on canonical sensors | 7 | 39.43 pp | 38.26 pp to 40.59 pp | 1.00 pp | pending |
| Randomized minus canonical on randomized sensors | 6 | 39.70 pp | 38.94 pp to 40.45 pp | 1.00 pp | pending |
| Canonical minus frozen | 0 | pending | — | 0.00 pp | pending |
| Canonical minus validation-selected shallow control | 0 | pending | — | 0.00 pp | pending |
| Canonical minus randomized on ciFAIR-10 | 0 | pending | — | 1.00 pp | pending |

## Counterfactual families and distribution shifts

| Learner | Sensor | Worlds | Test | Both mates | Unseen channels | Crowded | Constant | Known-filter oracle |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cd32 | cd32 | 7 | 89.97% | 83.30% | 89.48% | 88.25% | 50.00% | 93.79% |
| cd32 | random | 6 | 50.36% | 23.75% | 50.71% | 49.75% | 50.00% | 93.85% |
| random | cd32 | 7 | 50.54% | 21.32% | 50.43% | 49.45% | 50.00% | 93.79% |
| random | random | 6 | 90.06% | 83.87% | 89.96% | 88.81% | 50.00% | 93.85% |

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
