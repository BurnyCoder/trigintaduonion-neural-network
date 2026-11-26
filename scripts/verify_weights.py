"""Verify portable model files against one immutable public Hub revision."""
import argparse
import hashlib
import json
from pathlib import Path

from huggingface_hub import HfApi, hf_hub_download
import numpy as np
from safetensors import safe_open

from trig32.paths import CHECKPOINTS, RESULTS, write_json
from trig32.protocol import STAGES, runs
from trig32.reference import reference_table
from trig32.release import REPO


def verify_tables(weights, model, seed):
    """Reconstruct serialized routing against the independent data-side basis oracle."""
    signs = [key for key in weights.keys() if key.endswith(".sign")]
    if model in ("real", "budget", "shallow"):
        if signs:
            raise ValueError(f"{model} checkpoint contains an unexpected tied layer")
        return 0
    if not signs:
        raise ValueError(f"{model} checkpoint is missing its signed multiplication rule")
    dimension = 16 if model == "cd16" else 32
    rule = "random" if model == "random" else "cd32"
    table = reference_table(rule, seed)[:dimension, :dimension]
    inputs = np.arange(dimension)
    index = inputs[:, None] ^ inputs[None, :]
    for key in signs:
        np.testing.assert_array_equal(weights.get_tensor(key), table[index, inputs], err_msg=key)
        route = key.removesuffix(".sign") + ".index"
        np.testing.assert_array_equal(weights.get_tensor(route), index, err_msg=route)
    return len(signs)


def verify(run=None):
    """Use local training output when available, otherwise verify the downloaded checkpoint."""
    configs = {c.name: c for stage in STAGES for c in runs(stage)}
    if run and run not in configs:
        raise ValueError("specify a registered neural run")
    names = [run] if run else list(configs)
    # Algebra manifests identify every saved unrestricted bilinear and shuffled-target fit.
    if not run:
        for seed in range(8):
            records = json.loads((RESULTS / "algebra" / f"seed-{seed}.json").read_text())
            names.extend(f"product-{r['model']}-s{seed}-n{r['n']}" for r in records
                         if r["task"] == "product" and r["model"] in ("bilinear", "shuffled"))
    api = HfApi()
    revision = api.model_info(REPO).sha
    listing = api.list_repo_tree(REPO, path_in_repo="weights", recursive=True, revision=revision)
    remote = {f.path: f for f in listing if f.path.endswith("model.safetensors")}
    checked = {}
    for name in names:
        key = f"weights/{name}/model.safetensors"
        published = remote[key]
        local = CHECKPOINTS / name / "model.safetensors"
        source = "training output" if local.is_file() else "download"
        if not local.is_file():
            local = Path(hf_hub_download(REPO, key, revision=revision))
        with local.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        if digest != published.lfs.sha256 or local.stat().st_size != published.size:
            raise ValueError(f"public and local bytes differ for {name}")
        with safe_open(str(local), framework="np") as weights:
            if name in configs:
                c = configs[name]
                maps = verify_tables(weights, c.model, c.seed)
            else:
                if list(weights.get_slice("weight").get_shape()) != [32, 32, 32]:
                    raise ValueError(f"unexpected bilinear coefficient shape in {name}")
                maps = 0
        checked[name] = {"sha256": digest, "bytes": published.size, "source": source, "signed_maps": maps}
    neural = sum(n in configs for n in checked)
    return {"hub_revision": revision, "neural": neural, "algebra": len(checked)-neural,
            "signed_maps": sum(x["signed_maps"] for x in checked.values()), "weights": checked}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", help="check one registered neural checkpoint")
    parser.add_argument("--write", action="store_true", help="persist the complete release audit")
    args = parser.parse_args()
    if args.run and args.write:
        parser.error("--write requires the complete study")
    audit = verify(args.run)
    if args.write:
        write_json(RESULTS / "release-integrity.json", audit)
    print(json.dumps({k: v for k, v in audit.items() if k != "weights"}, indent=2))
