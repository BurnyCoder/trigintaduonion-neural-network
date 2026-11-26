"""Rebuilding a report for fresh outputs must not display numbers from an older study."""
from trig32 import figures as visuals
from trig32.protocol import Config
from trig32.report import benchmark_rows, estimate_remaining_training


def test_empty_outputs_drop_stale_result_figures(tmp_path, monkeypatch):
    """Keep the architecture and unrelated assets when a fresh output directory has no outcomes."""
    monkeypatch.setattr(visuals, "FIG", tmp_path)
    previous = ("scores", "effects", "learning", "example", "predictions", "sample-size",
                "gallery-graph", "gallery-pixel", "reading-swap")
    for name in (*previous, "independent"):
        (tmp_path / f"{name}.png").write_bytes(b"old")
    (tmp_path / "reading-swap.mp4").write_bytes(b"old")
    visuals.figures({"runs": [], "contrasts": []})
    assert (tmp_path / "architecture.png").is_file()
    assert (tmp_path / "independent.png").read_bytes() == b"old"
    assert all(not (tmp_path / f"{name}.png").exists() for name in previous)
    assert not (tmp_path / "reading-swap.mp4").exists()


def test_original_and_corrected_image_scores_remain_distinct():
    """Keep the original graph score, original pixel score and corrected pixel score in their proper columns."""
    graph={"config":{"task":"graph","model":"cd32"},"trainable":3500,
           "splits":{"test":{"accuracy":.60}}}
    pixel={"config":{"task":"pixel","model":"cd32"},"trainable":8000,
           "splits":{"test":{"accuracy":.80},"cifair":{"accuracy":.75}}}
    assert benchmark_rows({"runs":[graph,pixel]})==[
        ["graph","cd32",1,3500,"60.00%","—","—"],
        ["pixel","cd32",1,8000,"80.00%","75.00%","—"]]


def test_training_estimate_uses_comparable_completed_fits():
    """Prefer the same model, fall back within the task, and count budgets without observations."""
    completed = [
        {"config": vars(Config(task="pixel", model=model, epochs=60)), "seconds": seconds}
        for model, seconds in (("cd32", 10), ("cd32", 16), ("real", 30))
    ]
    pending = [Config(task="pixel", model=model, epochs=60) for model in ("cd32", "real", "random")]
    pending.extend([Config(task="graph", epochs=60), Config(task="pixel", epochs=80)])
    assert estimate_remaining_training(pending, completed) == (13 + 30 + 16, 3)
