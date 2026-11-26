# Literature review · 26 November 2026

The experiment asks whether knowing how sensor channels interact improves learning a spatial relation from scene-level supervision. Two distinct assumptions enter the model. Distances determine which entities should exchange information. A fixed multiplication table ties the channel coefficients used to interpret measurements.

| Family | What the original work tested | Relationship to this project |
|---|---|---|
| Real | LeCun et al. trained convolutional networks for document recognition. He et al. evaluated residual networks on CIFAR-10. | Real residual and graph networks are empirical comparators. [LeCun et al.](https://leon.bottou.org/papers/lecun-98h) · [He et al.](https://arxiv.org/abs/1512.03385) |
| Complex | Trabelsi et al. implemented complex convolution, normalization and initialization, including capacity-controlled image experiments. | A precedent for accounting for trainable real coefficients and for embedding algebra in ordinary tensor operations. [ICLR paper](https://arxiv.org/pdf/1705.09792) |
| Quaternion | Gaudet and Maida tested quaternion convolution on CIFAR-10/100. Zhu et al. separately used quaternion rotations and scalings of color vectors. | The first paper is closer to our left multiplication. Different quaternion parameterizations encode different assumptions. [Gaudet and Maida](https://arxiv.org/pdf/1712.04604) · [Zhu et al.](https://arxiv.org/abs/1903.00658) |
| Octonion | Wu et al. evaluated octonion convolution, normalization and initialization against lower-dimensional networks on CIFAR-10/100. | A direct image-classification precedent. Its performance estimates concern its own architectures and training recipe. [Published paper](https://doi.org/10.1016/j.neucom.2020.02.053) · [Open manuscript](https://arxiv.org/pdf/1903.08478) |
| Sedenion | Saoud and Al-Marzouqi evaluated a sedenion predictor for time series. Bojesomo et al. used sedenion convolutions for traffic forecasting. | The fifth doubling extends the 16-dimensional subalgebra these architectures use. [IEEE Access](https://doi.org/10.1109/ACCESS.2020.3014690) · [Bojesomo et al.](https://arxiv.org/pdf/2012.03874) |

### Geometry, algebra and controlled generalization

Biss, Dugger and Isaksen define a real Cayley–Dickson algebra recursively by (a,b)(c,d) = (ac − conjugate(d)b, da + b conjugate(c)). The fifth doubling gives 32 real components. Higher algebras have zero divisors and multiplication can depend on parenthesization. Saniga et al. describe the XOR index of each basis product and the triples of imaginary units. We use both the index and its sign. [Definition 2.1](https://arxiv.org/pdf/math/0511691) · [Finite geometry](https://arxiv.org/pdf/1405.6888)

CLEVR introduced scene programs that combine spatial selection and attribute comparison. Santoro et al. used nearest-object questions and relational controls. Our generator supplies object-level readings and a single binary label. It permits opposite-label examples with identical positions and identical measurement multisets. [CLEVR](https://cs.stanford.edu/people/jcjohns/clevr/) · [Relation networks](https://arxiv.org/pdf/1706.01427)

Gilmer et al. formalize learned messages, aggregation and readout. Satorras et al. use relative squared distances to construct Euclidean-equivariant updates. We keep positions fixed and use these distances in learned attention. Spatial isometries act on positions. The 32 coefficients are sensor features. [Message passing](https://proceedings.mlr.press/v70/gilmer17a.html) · [EGNN](https://proceedings.mlr.press/v139/satorras21a.html)

The research discipline follows explicit hypotheses, leakage checks and scope-limited claims. [Lones](https://arxiv.org/abs/2108.02497) · [Lipton and Steinhardt](https://arxiv.org/abs/1807.03341) · [NeurIPS checklist](https://neurips.cc/public/guides/PaperChecklist)
