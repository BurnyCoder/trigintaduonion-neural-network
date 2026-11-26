# Reproducing the study

Install uv and Python 3.12. Clone the research repository and run the commands below from its root. The lockfile pins PyTorch and the scalar algebra reference. An NVIDIA-compatible installation uses the CUDA 13.2 PyTorch wheel selected in pyproject.toml. The same models support CPU execution with `--device cpu`. Install pdfLaTeX with the geometry, graphicx, longtable and hyperref packages, or Tectonic, for paper regeneration. [uv](https://docs.astral.sh/uv/) · [PyTorch](https://pytorch.org/get-started/locally/) · [Tectonic](https://tectonic-typesetting.github.io/)

```sh
uv sync --frozen
uv run --no-sync pytest -q
uv run --no-sync trig32 dashboard
```

Open the dashboard at <http://127.0.0.1:18332/>. In another terminal run the pilot or the registered matrix. A local `.env` can set `TRIG32_DATA` and `TRIG32_CHECKPOINTS` to absolute paths on a larger drive. Local defaults are `data/` and `checkpoints/`. Inference accepts PyTorch tensors through the model classes and JSON or an RGB image through the CLI.

```sh
uv run trig32 train --task scene --model cd32 --rule cd32 --seed 42
uv run trig32 evaluate scene-cd32-cd32-s42-n1024
uv run trig32 predict scene-cd32-cd32-s42-n1024 --input results/scene-cd32-cd32-s42-n1024/test-examples.json --index 1
uv run trig32 algebra --seeds 0
uv run trig32 report
```

The train command samples independent family streams, runs the optimizer, logs validation metrics after each epoch, and saves the earliest best validation checkpoint. Reissue the exact command to resume. Test predictions and labels are written to compressed CSVs. The signed coefficient table is regenerated from the specified seed and also stored in the network's buffers. To load a published model, use its matching run manifest from the repository and pass its safetensors path via `predict --weights`. For natural images use `--input image.png`. For superpixels, select a graph with `--index`. The paper, explorer, raw tables, figure files and all per-experiment notebooks regenerate together with `trig32 report`.

### Data interface

A scene has two beacon positions `beacon[2,2]`, landmark coordinates `land[L,2]`, object coordinates `pos[O,2]`, Gaussian excitation `x[O,32]`, channel indices `k[O]` from 0 to 31, and corresponding signed noisy measurements `z[O]`. The public classifier returns one real logit per scene. Sigmoid produces the probability of equal types. The model accepts a variable object or landmark count shared across a batch. Split membership, hidden types, the world filter and selected neighbors are never model inputs. A model trained in one synthetic world may need retraining for a new filter. The independent clean-label oracle uses the full filter and exact nearest paths.

### Comparison arms and optimization

`cd32` ties channel coefficients according to the fifth Cayley–Dickson doubling. `random` uses identical XOR routing and a seeded sign intervention. `cd16` uses two 16-component groups within each width-32 feature vector. `real` uses unrestricted matrices. `budget` uses low-rank real maps on scenes and narrower real residual blocks on pixels. These capacity controls differ in rank or width. The JSON manifest records the actual coefficient counts. `frozen` fits only the scene readout. `onehop` severs the object-to-landmark path. `shallow` pools real nonlinear per-entity features with absolute coordinates and role indicators.

The primary budget targets sample-limited learning. A shared learning rate and schedule reduce tuning degrees of freedom in the crossover, and validation selection accommodates peaks before the final epoch. The learnable distance penalty begins at exp(4.5) on squared unit-square coordinates, favoring local messages from initialization. The paired samples always stay in one split. A fixed per-epoch seed controls shuffle and pixel augmentation during resumption. Each checkpoint stores the optimizer and scheduler as well as network state. Sources include [distance-conditioned graph updates](https://proceedings.mlr.press/v139/satorras21a.html), [AdamW](https://arxiv.org/abs/1711.05101) and [cosine annealing](https://docs.pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.CosineAnnealingLR.html).

### Full matrix and publication

```sh
uv run trig32 matrix --stage all
```

The full matrix trains the excluded pilot, runs the direct algebra diagnostics, freezes primary and control fits, evaluates the graph study, then runs the sample-size and external-image experiments. Individual stages are `pilot`, `primary`, `controls`, `sensitivity`, and `images`. The primary stage alone freezes checkpoints. The controls stage opens the registered test after the primary group has finished. The manual evaluate command is available for other studies. Exact study conditions are in the [run matrix](../reports/planned-runs.md).

The optional maintainer flag `--publish` commits scoped results to the configured Git origin and uses authenticated Hugging Face access to release weights. Ordinary reproduction runs locally. The dashboard reads live epoch JSON every five seconds. TensorBoard provides an alternative view through `uv run tensorboard --logdir logs/tensorboard`. Model training does not call an LLM. Timestamped stdout and JSONL files contain the run configuration, revision, measurements and device details.

Pixels and superpixels download on demand from the pinned upstream datasets. Pixel training uses reflected four-pixel padding, random crop and horizontal flip with normalization fitted only on its training partition. Count each exact pixel duplicate group once during split allocation. The fixed superpixel splits and ciFAIR test release are distinct evaluations. [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) · [Graph benchmark](https://www.jmlr.org/papers/v24/22-0567.html) · [ciFAIR](https://cvjena.github.io/cifair/)
