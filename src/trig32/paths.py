"""Project output locations and atomic, machine-readable records."""
import json
import os
import errno
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile

from dotenv import load_dotenv

ROOT = Path(os.environ.get("TRIG32_ROOT", Path.cwd())).resolve()
load_dotenv(ROOT / ".env")
DATA = Path(os.environ.get("TRIG32_DATA", ROOT / "data"))
CHECKPOINTS = Path(os.environ.get("TRIG32_CHECKPOINTS", ROOT / "checkpoints"))
OUTPUT = Path(os.environ.get("TRIG32_OUTPUT", ROOT))
RESULTS = OUTPUT / "results"
LOGS = OUTPUT / "logs"


def now():
    """Use UTC for interoperable experiment events."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def atomic_replace(source,destination):
    """Keep publication atomic when a short-lived Windows reader still holds the old file."""
    for attempt in range(10):
        try:
            os.replace(source,destination)
            return
        except PermissionError as exc:
            if getattr(exc,"winerror",None) not in (5,32,33) or attempt==9:
                raise
            time.sleep(min(.25,.01*2**attempt))


def write_json(path, value):
    """An interrupted update leaves the previous complete JSON document available."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(mode="w", dir=path.parent, encoding="utf-8", delete=False, suffix=".tmp") as f:
        json.dump(value, f, ensure_ascii=False, allow_nan=False, indent=2)
        f.write("\n")
    atomic_replace(f.name, path)


def log_event(run, **fields):
    """Persist and print identical, timestamped step-level or epoch-level measurements."""
    LOGS.mkdir(parents=True, exist_ok=True)
    record = {"time": now(), "run": run, **fields}
    line = json.dumps(record, ensure_ascii=False, allow_nan=False)
    with (LOGS / f"{run}.jsonl").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    try:
        print(line,flush=True)
    except OSError as exc:
        if exc.errno not in (errno.EBADF,errno.EPIPE):
            raise
        # A detached Windows launcher may close its stdout pipe while the epoch journal is healthy.
        sys.stdout=open(os.devnull,"w",encoding="utf-8")
    return record
