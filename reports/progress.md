# Study progress

Public preregistration at [4552d4d](https://github.com/BurnyCoder/trigintaduonion-neural-network/commit/4552d4d9bdd1465864d50c9e9bd429631ac2ae2c). The reproducible implementation, tests, paper source and explorer accompany the protocol. Completed training manifests: 99. Completed neural evaluations: 78. Completed algebra worlds: 8.

Across 8 independent simulated worlds, a network matched to the canonical sensor classified 90.04% (95% interval 89.28% to 90.79%) of held-out scenes correctly. A network matched to the randomized sensor classified 90.06% (95% interval 89.63% to 90.49%) correctly. The mean benefit of matching the sensor rule was 39.59 percentage points on canonical sensors and 39.58 points on randomized sensors. Both directional matching criteria passed.

78 of 99 planned neural evaluations are complete (78.79% by count). Different datasets require different amounts of compute. Mean fit time covers epoch loops and validation. Data preparation, evaluation and both public releases add wall time.

| Stage | Planned | Fitted | Tested | Tests remaining | Mean fit time |
| --- | --- | --- | --- | --- | --- |
| pilot | 1 | 1 | 1 | 0 | 33.0 s |
| primary | 32 | 32 | 32 | 0 | 26.0 s |
| controls | 33 | 33 | 33 | 0 | 14.8 s |
| sensitivity | 6 | 6 | 6 | 0 | 263.0 s |
| images | 27 | 27 | 6 | 21 | 843.8 s |

All checkpoints are frozen. Held-out evaluation and publication are in progress. [Planned runs](planned-runs.md) · [Experiments](experiments/experiments.md)
