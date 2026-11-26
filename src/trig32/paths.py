"""Project output locations and atomic, machine-readable records."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile

from dotenv import load_dotenv

ROOT = Path(os.environ.get("TRIG32_ROOT", Path.cwd())).resolve()
load_dotenv(ROOT / ".env")
DATA = Path(os.environ.get("TRIG32_DATA", ROOT / "data"))
CHECKPOINTS = Path(os.environ.get("TRIG32_CHECKPOINTS", ROOT / "checkpoints"))
RESULTS = ROOT / "results"
LOGS = ROOT / "logs"


def now():
    """Use UTC for interoperable experiment events."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def write_json(path, value):
    """An interrupted update leaves the previous complete JSON document available."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(mode="w", dir=path.parent, encoding="utf-8", delete=False, suffix=".tmp") as f:
        json.dump(value, f, ensure_ascii=False, allow_nan=False, indent=2)
        f.write("\n")
    os.replace(f.name, path)


def log_event(run, **fields):
    """Persist and print identical, timestamped step-level or epoch-level measurements."""
    LOGS.mkdir(parents=True, exist_ok=True)
    record = {"time": now(), "run": run, **fields}
    line = json.dumps(record, ensure_ascii=False, allow_nan=False)
    print(line, flush=True)
    with (LOGS / f"{run}.jsonl").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    return record
