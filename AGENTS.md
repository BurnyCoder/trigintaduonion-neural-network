# Working on this study

The [preregistration](reports/preregistration.md) fixes the questions, independent unit, model-selection rule and inferential thresholds. The [run matrix](reports/planned-runs.md) defines the arms. Preserve both when reproducing the study. Date post-hoc analyses and identify them in the paper.

Work from this directory in the uv environment. Place data, optimizer states and tokens outside version control. The [run guide](docs/usage.md) explains how to train into a fresh output directory, resume an epoch checkpoint, use the public weights and inspect live metrics.

Write tests before changing model or data semantics. Preserve the independent scalar implementation used for the scene renderer. The matrix fixes all primary and depth-control checkpoints before opening the confirmatory test outcomes.

Regenerate the public outputs with `uv run trig32 report`. Audit them independently with `uv run python scripts/verify_results.py --write`. Raw predictions, epoch logs and manifests are the sources for reported measurements. Change the reporting source when an edit must survive regeneration. Describe method changes and their timing in the [research reviews](reports/reviews/).
