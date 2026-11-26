"""Rebuilding a report for fresh outputs must not display numbers from an older study."""
from trig32 import figures as visuals
from trig32.report import benchmark_rows


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
