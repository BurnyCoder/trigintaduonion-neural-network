"""Reproduce the complete preregistered analysis from individual held-out decisions.

The study report reads evaluation manifests. This independent route reads prediction rows,
uses SciPy's one-sample t interval, and compares each seed and endpoint with the published result.
Protocol: https://github.com/BurnyCoder/trigintaduonion-neural-network/blob/4552d4d/reports/preregistration.md
"""
import argparse
import csv
from functools import cache
import gzip
import json

import numpy as np
from scipy.stats import ttest_1samp

from trig32.paths import RESULTS, ROOT, write_json
from trig32.protocol import Config


@cache
def accuracy(model, seed, rule="cd32", task="scene", split="test"):
    """Count correct decisions on the original CSV scale, independently of the evaluation summary."""
    run = Config(task=task, model=model, rule=rule, seed=seed).name
    with gzip.open(RESULTS / run / f"{split}-predictions.csv.gz", "rt", encoding="utf-8") as file:
        correct = [row["prediction"] == row["label"] for row in csv.DictReader(file)]
    return sum(correct) / len(correct)


def validation_winner(seed):
    """Reconstruct the shallow-control choice from validation records, including the tie rule."""
    def validation_score(model):
        run = Config(model=model, seed=seed).name
        return json.loads((RESULTS / run / "train.json").read_bytes())["val_accuracy"]

    return max(("onehop", "shallow"), key=validation_score)


def verify():
    """Check all paired values, interval endpoints, protocol thresholds and decisions."""
    registered = {
        "Matched canonical accuracy": (.60, lambda s: accuracy("cd32", s)),
        "Matched randomized accuracy": (.60, lambda s: accuracy("random", s, "random")),
        "Canonical minus randomized on canonical sensors":
            (.01, lambda s: accuracy("cd32", s) - accuracy("random", s)),
        "Randomized minus canonical on randomized sensors":
            (.01, lambda s: accuracy("random", s, "random") - accuracy("cd32", s, "random")),
        "Canonical minus frozen": (0., lambda s: accuracy("cd32", s) - accuracy("frozen", s)),
        "Canonical minus validation-selected shallow control":
            (0., lambda s: accuracy("cd32", s) - accuracy(validation_winner(s), s)),
        "Canonical minus randomized on ciFAIR-10":
            (.01, lambda s: accuracy("cd32", s, task="pixel", split="cifair")
                        - accuracy("random", s, task="pixel", split="cifair")),
    }
    released = {r["title"]: r for r in json.loads((ROOT / "docs/study.json").read_bytes())["contrasts"]}
    if registered.keys() != released.keys():
        raise ValueError("the released list of endpoints differs from the protocol")
    audit = {}
    for title, (threshold, compute) in registered.items():
        published = released[title]
        values = [compute(seed) for seed in range(8)]
        mean = float(np.mean(values))
        low, high = (ttest_1samp(values, 0).confidence_interval(.95)
                     if np.ptp(values) else (mean, mean))
        decision = "above threshold" if low > threshold else "below threshold" if high < threshold else "inconclusive"
        if published["n"] != len(values) or published["threshold"] != threshold or published["decision"] != decision:
            raise ValueError(f"{title} has inconsistent replication, threshold or decision")
        # Decimal publication uses the stored full precision; the rendered tables round for readability.
        np.testing.assert_allclose(values, [published["values"][str(i)] for i in range(len(values))],
                                   atol=1e-12, rtol=0, err_msg=title)
        np.testing.assert_allclose([mean, low, high], [published[k] for k in ("mean", "lo", "hi")],
                                   atol=1e-12, rtol=0, err_msg=title)
        audit[title] = dict(seed_values=values, mean=mean, low=float(low), high=float(high),
                            threshold=threshold, decision=decision)
    return audit


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="save results/contrast-audit.json")
    args = parser.parse_args()
    result = verify()
    if args.write:
        write_json(RESULTS / "contrast-audit.json", result)
    print(json.dumps(result, indent=2))
