# Results

Across 8 independent simulated worlds, a network matched to the canonical sensor classified 90.04% (95% interval 89.28% to 90.79%) of held-out scenes correctly. A network matched to the randomized sensor classified 90.06% (95% interval 89.63% to 90.49%) correctly. The mean benefit of matching the sensor rule was 39.59 percentage points on canonical sensors and 39.58 points on randomized sensors. Both directional matching criteria passed.

On canonical scenes the full network's paired accuracy difference was +39.48 points against the frozen encoder and +40.08 points against the validation-selected shallow control. Both lower bounds exceeded zero.

On the 3 canonical worlds shared by the capacity baselines, mean test accuracy was 90.28% for the trigintaduonion network, 61.90% for the sedenion network, 50.05% for unrestricted real maps and 49.92% for low-rank real maps. These comparisons are descriptive.

In the single-world data-size study, increasing training from 256 to 32,768 families changed canonical accuracy from 56.10% to 92.97% and randomized accuracy from 51.12% to 54.93%. The larger conditions also used more optimizer updates under the fixed epoch budget.

On the corrected natural-image test set, the paired difference for canonical minus randomized sharing was -0.28 points (95% interval -0.80 to +0.24). The upper bound rules out a one-point canonical advantage for this training recipe.

| Task / learner / sensor | Tested worlds | Trainable | Mean test | 95% interval |
| --- | --- | --- | --- | --- |
| graph / cd32 | 1 | 1694 | 34.80% | — |
| graph / random | 1 | 1694 | 34.55% | — |
| pixel / budget | 1 | 13115 | 78.23% | — |
| pixel / cd16 | 1 | 22570 | 82.01% | — |
| pixel / cd32 | 8 | 13034 | 78.80% | 78.47% to 79.14% |
| pixel / random | 8 | 13034 | 79.06% | 78.63% to 79.48% |
| pixel / real | 1 | 308650 | 90.33% | — |
| scene / budget / cd32 / 1024 families | 3 | 3961 | 49.92% | 47.73% to 52.10% |
| scene / cd16 / cd32 / 1024 families | 3 | 4057 | 61.90% | 48.57% to 75.22% |
| scene / cd32 / cd32 / 1024 families | 8 | 3801 | 90.04% | 89.28% to 90.79% |
| scene / cd32 / cd32 / 256 families | 1 | 3801 | 56.10% | — |
| scene / cd32 / cd32 / 32768 families | 1 | 3801 | 92.97% | — |
| scene / cd32 / cd32 / 4096 families | 1 | 3801 | 92.29% | — |
| scene / cd32 / cd32 / 1024 families (pilot) | 1 | 3801 | 89.16% | — |
| scene / cd32 / random / 1024 families | 8 | 3801 | 50.49% | 49.82% to 51.15% |
| scene / frozen / cd32 / 1024 families | 8 | 2113 | 50.56% | 50.10% to 51.01% |
| scene / onehop / cd32 / 1024 families | 8 | 3801 | 50.00% | 50.00% to 50.00% |
| scene / random / cd32 / 1024 families | 8 | 3801 | 50.45% | 49.75% to 51.14% |
| scene / random / cd32 / 256 families | 1 | 3801 | 51.12% | — |
| scene / random / cd32 / 32768 families | 1 | 3801 | 54.93% | — |
| scene / random / cd32 / 4096 families | 1 | 3801 | 50.88% | — |
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
| Canonical minus randomized on ciFAIR-10 | 8 | -0.28 pp | -0.80 pp to 0.24 pp | 1.00 pp | below threshold |

## Counterfactual families and distribution shifts

| Learner | Sensor | Worlds | Test | Both mates | Unseen channels | Crowded | Constant | Known-filter oracle |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| budget | cd32 | 3 | 49.92% | 21.65% | 50.23% | 48.86% | 50.00% | 93.62% |
| cd16 | cd32 | 3 | 61.90% | 38.90% | 61.88% | 61.74% | 50.00% | 93.62% |
| cd32 | cd32 | 8 | 90.04% | 83.53% | 89.68% | 88.53% | 50.00% | 93.74% |
| cd32 | random | 8 | 50.49% | 22.88% | 50.69% | 50.07% | 50.00% | 93.83% |
| frozen | cd32 | 8 | 50.56% | 15.01% | 49.57% | 50.75% | 50.00% | 93.74% |
| onehop | cd32 | 8 | 50.00% | 0.00% | 50.00% | 50.00% | 50.00% | 93.74% |
| random | cd32 | 8 | 50.45% | 21.62% | 50.23% | 49.65% | 50.00% | 93.74% |
| random | random | 8 | 90.06% | 83.72% | 90.14% | 89.09% | 50.00% | 93.83% |
| real | cd32 | 3 | 50.05% | 18.98% | 50.29% | 50.63% | 50.00% | 93.62% |
| shallow | cd32 | 8 | 49.96% | 0.13% | 50.00% | 49.98% | 50.00% | 93.74% |

Each entry averages the saved world-level scores. Both mates counts families whose two opposite labels were both predicted correctly. The last two columns evaluate analytic controls on the original test scenes.

## Independent image benchmarks

| Input | Learner | Seeds | Trainable | CIFAR-10 | ciFAIR-10 | ciFAIR 95% interval |
| --- | --- | --- | --- | --- | --- | --- |
| graph | cd32 | 1 | 1694 | 34.80% | — | — |
| graph | random | 1 | 1694 | 34.55% | — | — |
| pixel | budget | 1 | 13115 | 78.23% | 77.20% | — |
| pixel | cd16 | 1 | 22570 | 82.01% | 81.02% | — |
| pixel | cd32 | 8 | 13034 | 78.80% | 77.73% | 77.43% to 78.02% |
| pixel | random | 8 | 13034 | 79.06% | 78.01% | 77.60% to 78.42% |
| pixel | real | 1 | 308650 | 90.33% | 89.54% | — |

## Supplementary fixed-checkpoint interventions

| Run | Input | Accuracy against original labels | Decisions changed | Max Δ probability |
| --- | --- | --- | --- | --- |
| scene-cd32-cd32-s42-n1024 | original | 89.16% | 0 | 0 |
| scene-cd32-cd32-s42-n1024 | isometry_and_reindexing | 89.16% | 0 | 0.0306 |
| scene-cd32-cd32-s42-n1024 | broken_correspondence | 49.85% | 1009 | 1 |

The float64 symmetry reference for scene-cd32-cd32-s42-n1024 changed 0 decisions. Maximum absolute probability drift was 2.61e-14.

Scene intervals use a two-sided Student t across independent worlds. Each image seed evaluates the same images, so the image interval measures training variability conditional on that test set. Differences use percentage points. A single seed has no between-seed interval. The pilot is excluded from all confirmatory contrasts.

[Raw manifests and predictions](../results/) · [Preregistration](preregistration.md) · [Explorer](https://burnycoder.github.io/trigintaduonion-neural-network/)
