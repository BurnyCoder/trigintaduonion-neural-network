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
The pilot has no released test prediction yet. The registered crossover awaits complete paired worlds. [All measured outcomes](https://burnycoder.github.io/trigintaduonion-neural-network/)
<!-- metrics:end -->
