---
license: mit
library_name: pytorch
tags:
- geometric-deep-learning
- hypercomplex
- image-classification
---

# Trigintaduonion neural network

This collection repository stores portable PyTorch weights, source code, the versioned protocol, and regenerable evaluations for geometric reasoning with 32-component sensors. Each named checkpoint has its architecture, numerical environment and seed in the corresponding results directory. A trained scene model accepts ordered sensor coordinates in a specific simulated world.

[Research repository](https://github.com/BurnyCoder/trigintaduonion-neural-network) · [Study explorer](https://burnycoder.github.io/trigintaduonion-neural-network/) · [Evaluation protocol](reports/preregistration.md)

Use the source CLI with a matching run manifest and the safetensors file from its weights directory. Example: `uv run trig32 predict scene-cd32-cd32-s42-n1024 --weights downloaded-model.safetensors --input scene.json`. Published example JSON contains batched scenes, selected by the optional index. The scores below are generated from saved results.

<!-- metrics:start -->
Across 8 independent simulated worlds, a network matched to the canonical sensor classified 90.04% (95% interval 89.28% to 90.79%) of held-out scenes correctly. A network matched to the randomized sensor classified 90.06% (95% interval 89.63% to 90.49%) correctly. The mean benefit of matching the sensor rule was 39.59 percentage points on canonical sensors and 39.58 points on randomized sensors. Both directional matching criteria passed. On the corrected natural-image test set, the paired difference for canonical minus randomized sharing was -0.28 points (95% interval -0.80 to +0.24). The upper bound rules out a one-point canonical advantage for this training recipe. [All measured outcomes](https://burnycoder.github.io/trigintaduonion-neural-network/)
<!-- metrics:end -->
