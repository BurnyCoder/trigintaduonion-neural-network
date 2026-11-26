# Research observations

Across 8 independent simulated worlds, a network matched to the canonical sensor classified 90.04% (95% interval 89.28% to 90.79%) of held-out scenes correctly. A network matched to the randomized sensor classified 90.06% (95% interval 89.63% to 90.49%) correctly. The mean benefit of matching the sensor rule was 39.59 percentage points on canonical sensors and 39.58 points on randomized sensors. Both directional matching criteria passed.

On canonical scenes the full network's paired accuracy difference was +39.48 points against the frozen encoder and +40.08 points against the validation-selected shallow control. Both lower bounds exceeded zero.

On the 3 canonical worlds shared by the capacity baselines, mean test accuracy was 90.28% for the trigintaduonion network, 61.90% for the sedenion network, 50.05% for unrestricted real maps and 49.92% for low-rank real maps. These comparisons are descriptive.

In the single-world data-size study, increasing training from 256 to 32,768 families changed canonical accuracy from 56.10% to 92.97% and randomized accuracy from 51.12% to 54.93%. The larger conditions also used more optimizer updates under the fixed epoch budget.

On the corrected natural-image test set, the paired difference for canonical minus randomized sharing was -0.28 points (95% interval -0.80 to +0.24). The upper bound rules out a one-point canonical advantage for this training recipe.

The independent scalar implementation supplies rendering ground truth. Reversing high-basis triples changes coordinate interaction signs while preserving routing, real dimension and the lower subalgebra. An exact multiplier fit tests implementation and identifiability. Generalization of the full scene classifier requires separate held-out predictions.

[Prior methods](../state-of-the-art-review.md) · [Per-run outcomes](experiments.md)
