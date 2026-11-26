# Results

Across 8 independent simulated worlds, a network matched to the canonical sensor classified 90.04% (95% interval 89.28% to 90.79%) of held-out scenes correctly. A network matched to the randomized sensor classified 90.06% (95% interval 89.63% to 90.49%) correctly. The mean benefit of matching the sensor rule was 39.59 percentage points on canonical sensors and 39.58 points on randomized sensors. Both directional matching criteria passed.

On canonical scenes the full network's paired accuracy difference was +39.48 points against the frozen encoder and +40.08 points against the validation-selected shallow control. Both lower bounds exceeded zero.

| Task / learner / sensor | Tested worlds | Trainable | Mean test | 95% interval |
| --- | --- | --- | --- | --- |
| scene / budget / cd32 / 1024 families | 3 | 3961 | 49.92% | 47.73% to 52.10% |
| scene / cd16 / cd32 / 1024 families | 2 | 4057 | 64.89% | 47.52% to 82.26% |
| scene / cd32 / cd32 / 1024 families | 8 | 3801 | 90.04% | 89.28% to 90.79% |
| scene / cd32 / cd32 / 1024 families (pilot) | 1 | 3801 | 89.16% | — |
| scene / cd32 / random / 1024 families | 8 | 3801 | 50.49% | 49.82% to 51.15% |
| scene / frozen / cd32 / 1024 families | 8 | 2113 | 50.56% | 50.10% to 51.01% |
| scene / onehop / cd32 / 1024 families | 8 | 3801 | 50.00% | 50.00% to 50.00% |
| scene / random / cd32 / 1024 families | 8 | 3801 | 50.45% | 49.75% to 51.14% |
| scene / random / random / 1024 families | 8 | 3801 | 90.06% | 89.63% to 90.49% |
| scene / real / cd32 / 1024 families | 3 | 11737 | 50.05% | 47.93% to 52.16% |
| scene / shallow / cd32 / 1024 families | 8 | 7713 | 49.96% | 49.89% to 50.03% |

| Registered endpoint | Worlds | Estimate | 95% interval | Threshold | Decision |
| --- | --- | --- | --- | --- | --- |
| Matched canonical accuracy | 8 | 90.04% | 89.28% to 90.79% | 60.00% | above threshold |
| Matched randomized accuracy | 8 | 90.06% | 89.63% to 90.49% | 60.00% | above threshold |
| Canonical minus randomized on canonical sensors | 8 | 39.59 pp | 38.54 pp to 40.65 pp | 1.00 pp | above threshold |
| Randomized minus canonical on randomized sensors | 8 | 39.58 pp | 38.96 pp to 40.19 pp | 1.00 pp | above threshold |
| Canonical minus frozen | 8 | 39.48 pp | 38.82 pp to 40.15 pp | 0.00 pp | above threshold |
| Canonical minus validation-selected shallow control | 8 | 40.08 pp | 39.33 pp to 40.84 pp | 0.00 pp | above threshold |
| Canonical minus randomized on ciFAIR-10 | 0 | pending | — | 1.00 pp | pending |

## Counterfactual families and distribution shifts

| Learner | Sensor | Worlds | Test | Both mates | Unseen channels | Crowded | Constant | Known-filter oracle |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| budget | cd32 | 3 | 49.92% | 21.65% | 50.23% | 48.86% | 50.00% | 93.62% |
| cd16 | cd32 | 2 | 64.89% | 43.02% | 64.33% | 65.14% | 50.00% | 93.68% |
| cd32 | cd32 | 8 | 90.04% | 83.53% | 89.68% | 88.53% | 50.00% | 93.74% |
| cd32 | random | 8 | 50.49% | 22.88% | 50.69% | 50.07% | 50.00% | 93.83% |
| frozen | cd32 | 8 | 50.56% | 15.01% | 49.57% | 50.75% | 50.00% | 93.74% |
| onehop | cd32 | 8 | 50.00% | 0.00% | 50.00% | 50.00% | 50.00% | 93.74% |
| random | cd32 | 8 | 50.45% | 21.62% | 50.23% | 49.65% | 50.00% | 93.74% |
| random | random | 8 | 90.06% | 83.72% | 90.14% | 89.09% | 50.00% | 93.83% |
| real | cd32 | 3 | 50.05% | 18.98% | 50.29% | 50.63% | 50.00% | 93.62% |
| shallow | cd32 | 8 | 49.96% | 0.13% | 50.00% | 49.98% | 50.00% | 93.74% |

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
