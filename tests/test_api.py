import os, io, tempfile, shutil
from fastapi.testclient import TestClient


os.environ["DATABASE_URL"] = "sqlite:///./test_api.db"


_tempdir = tempfile.mkdtemp(prefix="uploads_test_")
os.environ["UPLOAD_DIR"] = _tempdir

from app.main import app  
client = TestClient(app)

def teardown_module(module=None):
    try:
        shutil.rmtree(_tempdir, ignore_errors=True)
        if os.path.exists("./test_api.db"):
            os.remove("./test_api.db")
    except Exception:
        pass

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_upload_list_download():
    data = b"hello world"
    r = client.post("/upload", files={"file": ("hello.txt", io.BytesIO(data), "text/plain")})
    assert r.status_code == 200, r.text
    fid = r.json()["id"]

    r2 = client.get("/files")
    assert r2.status_code == 200
    assert any(x["id"] == fid for x in r2.json())

    r3 = client.get(f"/files/{fid}")
    assert r3.status_code == 200
    assert r3.content == data

def test_oversize():
    big = b"x" * (20 * 1024 * 1024 + 1)  # > 20MB
    r = client.post("/upload", files={"file": ("big.bin", io.BytesIO(big), "application/octet-stream")})
    assert r.status_code == 400

def test_not_found():
    r = client.get("/files/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404
