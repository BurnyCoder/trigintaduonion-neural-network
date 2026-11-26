# Results

Across 8 independent simulated worlds, a network matched to the canonical sensor classified 90.04% (95% interval 89.28% to 90.79%) of held-out scenes correctly. A network matched to the randomized sensor classified 90.06% (95% interval 89.63% to 90.49%) correctly. The mean benefit of matching the sensor rule was 39.59 percentage points on canonical sensors and 39.58 points on randomized sensors. Both directional matching criteria passed.

| Task / learner / sensor | Tested worlds | Trainable | Mean test | 95% interval |
| --- | --- | --- | --- | --- |
| scene / budget / cd32 / 1024 families | 0 | 3961 | pending | — |
| scene / cd16 / cd32 / 1024 families | 0 | 4057 | pending | — |
| scene / cd32 / cd32 / 1024 families | 8 | 3801 | 90.04% | 89.28% to 90.79% |
| scene / cd32 / cd32 / 1024 families (pilot) | 1 | 3801 | 89.16% | — |
| scene / cd32 / random / 1024 families | 8 | 3801 | 50.49% | 49.82% to 51.15% |
| scene / frozen / cd32 / 1024 families | 7 | 2113 | 50.57% | 50.02% to 51.11% |
| scene / onehop / cd32 / 1024 families | 0 | 3801 | pending | — |
| scene / random / cd32 / 1024 families | 8 | 3801 | 50.45% | 49.75% to 51.14% |
| scene / random / random / 1024 families | 8 | 3801 | 90.06% | 89.63% to 90.49% |
| scene / real / cd32 / 1024 families | 0 | 11737 | pending | — |
| scene / shallow / cd32 / 1024 families | 0 | 7713 | pending | — |

| Registered endpoint | Worlds | Estimate | 95% interval | Threshold | Decision |
| --- | --- | --- | --- | --- | --- |
| Matched canonical accuracy | 8 | 90.04% | 89.28% to 90.79% | 60.00% | above threshold |
| Matched randomized accuracy | 8 | 90.06% | 89.63% to 90.49% | 60.00% | above threshold |
| Canonical minus randomized on canonical sensors | 8 | 39.59 pp | 38.54 pp to 40.65 pp | 1.00 pp | above threshold |
| Randomized minus canonical on randomized sensors | 8 | 39.58 pp | 38.96 pp to 40.19 pp | 1.00 pp | above threshold |
| Canonical minus frozen | 7 | 39.40 pp | 38.64 pp to 40.17 pp | 0.00 pp | pending |
| Canonical minus validation-selected shallow control | 0 | pending | — | 0.00 pp | pending |
| Canonical minus randomized on ciFAIR-10 | 0 | pending | — | 1.00 pp | pending |

## Counterfactual families and distribution shifts

| Learner | Sensor | Worlds | Test | Both mates | Unseen channels | Crowded | Constant | Known-filter oracle |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cd32 | cd32 | 8 | 90.04% | 83.53% | 89.68% | 88.53% | 50.00% | 93.74% |
| cd32 | random | 8 | 50.49% | 22.88% | 50.69% | 50.07% | 50.00% | 93.83% |
| frozen | cd32 | 7 | 50.57% | 14.90% | 49.69% | 50.67% | 50.00% | 93.79% |
| random | cd32 | 8 | 50.45% | 21.62% | 50.23% | 49.65% | 50.00% | 93.74% |
| random | random | 8 | 90.06% | 83.72% | 90.14% | 89.09% | 50.00% | 93.83% |

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
