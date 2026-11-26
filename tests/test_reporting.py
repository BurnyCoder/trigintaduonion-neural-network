"""Rebuilding a report for fresh outputs must not display numbers from an older study."""
from trig32 import figures as visuals


def test_empty_outputs_drop_stale_result_figures(tmp_path, monkeypatch):
    """Keep the architecture and unrelated assets when a fresh output directory has no outcomes."""
    monkeypatch.setattr(visuals, "FIG", tmp_path)
    previous = ("scores", "effects", "learning", "example", "predictions", "sample-size",
                "gallery-graph", "gallery-pixel")
    for name in (*previous, "independent"):
        (tmp_path / f"{name}.png").write_bytes(b"old")
    visuals.figures({"runs": [], "contrasts": []})
    assert (tmp_path / "architecture.png").is_file()
    assert (tmp_path / "independent.png").read_bytes() == b"old"
    assert all(not (tmp_path / f"{name}.png").exists() for name in previous)
