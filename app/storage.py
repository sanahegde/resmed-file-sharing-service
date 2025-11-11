import os, time, uuid
from pathlib import Path
from .settings import UPLOAD_DIR, MAX_UPLOAD_BYTES

def new_id() -> str:
    return str(uuid.uuid4())

def ext_from(name: str) -> str:
    _, ext = os.path.splitext(name or "")
    return ext if ext else ".bin"

def now_unix() -> int:
    return int(time.time())

def save_stream(fileobj, dest: Path, max_bytes: int = MAX_UPLOAD_BYTES) -> int:
    """Stream to disk (1MB chunks), enforce max_bytes, delete partial if exceeded."""
    size = 0
    with dest.open("wb") as out:
        while True:
            chunk = fileobj.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            if size > max_bytes:
                out.close()
                dest.unlink(missing_ok=True)
                raise ValueError("file too large")
            out.write(chunk)
    return size
