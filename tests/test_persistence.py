"""Check the real Windows reader/atomic-replace failure observed with the live monitor."""
from trig32 import paths


def test_reader_share_retry(tmp_path,monkeypatch):
    destination=tmp_path/"live.json"
    destination.write_text("old")
    original=paths.os.replace
    calls=[]
    def transient(source,dest):
        calls.append(dest)
        if len(calls)==1:
            error=PermissionError("temporarily shared by monitor")
            error.winerror=32
            raise error
        original(source,dest)
    monkeypatch.setattr(paths.os,"replace",transient)
    paths.write_json(destination,{"epoch":6})
    assert len(calls)==2 and paths.json.loads(destination.read_text())=={"epoch":6}
