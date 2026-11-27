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

Install FFmpeg with its H.264 encoder to regenerate the optional counterfactual MP4 with `uv run trig32 report`. The two endpoint probabilities come from the first fixed pilot pair. The moving markers illustrate the exchange between those recorded scenes. [Matplotlib movie writer](https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FFMpegWriter.html) · [FFmpeg](https://ffmpeg.org/)

For an independent fit in a clone that already contains released metrics, set `TRIG32_OUTPUT` and `TRIG32_CHECKPOINTS` to fresh directories in .env. The first directory holds the new results and logs. A published checkpoint can be fetched automatically by the prediction command when its manifest is present and the weights are absent. Run `uv run trig32 audit scene-cd32-cd32-s42-n1024` to recount every saved decision and measure the effect of spatial interventions on that fixed checkpoint.

A scene has two beacon positions `beacon[2,2]`, landmark coordinates `land[L,2]`, object coordinates `pos[O,2]`, Gaussian excitation `x[O,32]`, channel indices `k[O]` from 0 to 31, and corresponding signed noisy measurements `z[O]`. The public classifier returns one real logit per scene. Sigmoid produces the probability of equal types. The model accepts a variable object or landmark count shared across a batch. Split membership, hidden types, the world filter and selected neighbors are never model inputs. A model trained in one synthetic world may need retraining for a new filter. The independent clean-label oracle uses the full filter and exact nearest paths.

### Using the PyTorch modules

The linear layer maps groups of 32 real components to new groups of 32. For convolution, place the components consecutively in the ordinary PyTorch channel axis. Left multiplication fixes the operand order throughout both layers.

```python
import torch
from trig32.algebra import CD32Conv2d, CD32Linear

linear = CD32Linear(2, 3)
assert linear(torch.randn(5, 2, 32)).shape == (5, 3, 32)
conv = CD32Conv2d(1, 2, 3, padding=1)
assert conv(torch.randn(5, 32, 8, 8)).shape == (5, 64, 8, 8)
```

The spatial classifier accepts the feature dictionary above. This example differentiates the complete encoder, both message blocks and the scene head using the final equality labels. Use the training CLI for optimizer steps, checkpoint selection and evaluation.

```python
import torch
from torch.nn.functional import binary_cross_entropy_with_logits
from trig32.models import SceneClassifier
from trig32.scenes import SceneSet

torch.manual_seed(7)
scenes = SceneSet(families=2, seed=7, split="train", rule="cd32")
features, targets = scenes.batch(torch.arange(len(scenes)))
model = SceneClassifier(kind="cd32", seed=7)
logits = model(features)
binary_cross_entropy_with_logits(logits, targets).backward()
```

### Comparison arms and optimization

For external superpixel inference, pass JSON with normalized `x[N,3]` RGB means, unit-square `pos[N,2]`, and zero-based directed `edge[2,E]` source/destination indices. The graph readout returns ten class probabilities. The natural-image explorer shows fixed inputs with their true labels, predicted labels and confidence.

`cd32` ties channel coefficients according to the fifth Cayley–Dickson doubling. `random` uses identical XOR routing and a seeded sign intervention. `cd16` uses two 16-component groups within each width-32 feature vector. `real` uses unrestricted matrices. `budget` uses low-rank real maps on scenes and narrower real residual blocks on pixels. These capacity controls differ in rank or width. The JSON manifest records the actual coefficient counts. `frozen` fits only the scene readout. `onehop` severs the object-to-landmark path. `shallow` pools real nonlinear per-entity features with absolute coordinates and role indicators.

The primary budget targets sample-limited learning. A shared learning rate and schedule reduce tuning degrees of freedom in the crossover, and validation selection accommodates peaks before the final epoch. The learnable distance penalty begins at exp(4.5) on squared unit-square coordinates, favoring local messages from initialization. The paired samples always stay in one split. A fixed per-epoch seed controls shuffle and pixel augmentation during resumption. Each checkpoint stores the optimizer and scheduler as well as network state. Sources include [distance-conditioned graph updates](https://proceedings.mlr.press/v139/satorras21a.html), [AdamW](https://arxiv.org/abs/1711.05101) and [cosine annealing](https://docs.pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.CosineAnnealingLR.html).

### Full matrix and publication

```sh
uv run trig32 matrix --stage all
```

The full matrix trains the excluded pilot, runs the direct algebra diagnostics, freezes primary and control fits, evaluates the graph study, then runs the sample-size and external-image experiments. Individual stages are `pilot`, `primary`, `controls`, `sensitivity`, and `images`. The primary stage alone freezes checkpoints. The controls stage opens the registered test after the primary group has finished. The manual evaluate command is available for other studies. Exact study conditions are in the [run matrix](../reports/planned-runs.md).

The optional maintainer flag `--publish` commits scoped results to the configured Git origin and uses authenticated Hugging Face access to release weights. Ordinary reproduction runs locally. The dashboard reads live epoch JSON every five seconds. TensorBoard provides an alternative view through `uv run tensorboard --logdir logs/tensorboard`. Model training does not call an LLM. Timestamped stdout and JSONL files contain the run configuration, revision, measurements and device details.

Run `uv run trig32 data-audit` to prepare all public benchmark inputs and verify exact pixel-group separation, RGB moments, graph offsets and class counts. It writes the resulting source revisions and counts to the results directory. A scene checkpoint audit also recomputes geometric interventions on CPU in float64, using identical trained weights, to quantify the effect of working precision.

Run `uv run python scripts/verify_results.py --write` to independently recount released predictions, check the held-out label sequence across paired conditions and verify validation-selected epochs. The auditor compares the final checkpoint timestamp with the first evaluation separately for the registered scene and external image comparisons. Partial runs are explicitly counted.

For the complete study, `uv run python scripts/verify_contrasts.py --write` reconstructs each registered estimate from the saved individual predictions. It checks each seed, recomputes the paired confidence intervals using SciPy and verifies the decisions against the public protocol and explorer.

Run `uv run python scripts/verify_weights.py --run scene-cd32-cd32-s42-n1024` to compare the exported checkpoint's SHA-256 with the public Hub revision and check every signed layer against the independent basis oracle. A fresh clone downloads the checkpoint automatically. After the full matrix is available, `uv run python scripts/verify_weights.py --write` verifies every registered neural and bilinear checkpoint and records the hashes.

Pixels and superpixels download on demand from the pinned upstream datasets. Pixel training uses reflected four-pixel padding, random crop and horizontal flip with normalization fitted only on its training partition. Count each exact pixel duplicate group once during split allocation. The fixed superpixel splits and ciFAIR test release are distinct evaluations. [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) · [Graph benchmark](https://www.jmlr.org/papers/v24/22-0567.html) · [ciFAIR](https://cvjena.github.io/cifair/)
