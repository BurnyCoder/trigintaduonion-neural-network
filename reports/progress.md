# Study progress

Public preregistration at [4552d4d](https://github.com/BurnyCoder/trigintaduonion-neural-network/commit/4552d4d9bdd1465864d50c9e9bd429631ac2ae2c). The reproducible implementation, tests, paper source and explorer accompany the protocol. Completed training manifests: 99. Completed neural evaluations: 99. Completed algebra worlds: 8.

Across 8 independent simulated worlds, a network matched to the canonical sensor classified 90.04% (95% interval 89.28% to 90.79%) of held-out scenes correctly. A network matched to the randomized sensor classified 90.06% (95% interval 89.63% to 90.49%) correctly. The mean benefit of matching the sensor rule was 39.59 percentage points on canonical sensors and 39.58 points on randomized sensors. Both directional matching criteria passed. On the corrected natural-image test set, the paired difference for canonical minus randomized sharing was -0.28 points (95% interval -0.80 to +0.24). The upper bound rules out a one-point canonical advantage for this training recipe.

99 of 99 planned neural evaluations are complete (100.00% by count). Different datasets require different amounts of compute. Mean fit time covers epoch loops and validation. Data preparation, evaluation and both public releases add wall time.

| Stage | Planned | Fitted | Tested | Tests remaining | Mean fit time |
| --- | --- | --- | --- | --- | --- |
| pilot | 1 | 1 | 1 | 0 | 33.0 s |
| primary | 32 | 32 | 32 | 0 | 26.0 s |
| controls | 33 | 33 | 33 | 0 | 14.8 s |
| sensitivity | 6 | 6 | 6 | 0 | 263.0 s |
| images | 27 | 27 | 27 | 0 | 843.8 s |

All registered neural evaluations are complete. Logged training and validation took 7.14 cumulative epoch-loop hours. The longest fit was pixel-cd32-cd32-s0 at 17.4 minutes. [Raw prediction recount](../results/recount.json) [Planned runs](planned-runs.md) · [Experiments](experiments/experiments.md)
