from pathlib import Path
from fastapi import FastAPI, UploadFile, File as FormFile, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from pathlib import Path


from .settings import UPLOAD_DIR, MAX_UPLOAD_BYTES
from .db import SessionLocal, init_db
from .models import FileMeta
from .storage import new_id, ext_from, save_stream, now_unix
from .errors import unhandled_exception_handler

app = FastAPI(
    title="File Sharing API",
    version="1.0.0",
    description="Upload (≤20MB), list metadata, and download files. Stores bytes on disk; metadata in Postgres."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.add_exception_handler(Exception, unhandled_exception_handler)

@app.on_event("startup")
def startup():
    init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post("/upload")
def upload(file: UploadFile = FormFile(...), db: Session = Depends(get_db)):
    """Accept multipart/form-data with field 'file'. Returns file id and metadata."""
    if not file:
        raise HTTPException(status_code=400, detail="file required")

    fid = new_id()
    ext = ext_from(file.filename)
    stored = f"{fid}{ext}"
    dest = UPLOAD_DIR / stored

    try:
        size = save_stream(file.file, dest) 
    except ValueError:
        raise HTTPException(status_code=400, detail=f"file too large (limit {MAX_UPLOAD_BYTES // (1024*1024)}MB)")
    except Exception:
        dest.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail="internal error")

    meta = FileMeta(
        id=fid, name=file.filename or f"upload{ext}",
        path=str(dest), size=size, uploaded_at=now_unix()
    )
    db.add(meta)
    db.commit()

    return {"id": meta.id, "name": meta.name, "size": meta.size, "uploaded_at": meta.uploaded_at}

@app.get("/files")
def list_files(db: Session = Depends(get_db)):
    rows = db.query(FileMeta).order_by(FileMeta.uploaded_at.desc()).all()
    return [
        {"id": r.id, "name": r.name, "size": r.size, "uploaded_at": r.uploaded_at}
        for r in rows
    ]

@app.get("/files/{file_id}")
def download(file_id: str, db: Session = Depends(get_db)):
    row = db.get(FileMeta, file_id)
    if not row:
        raise HTTPException(status_code=404, detail="file not found")

    path = Path(row.path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="file not found")

    return FileResponse(path, filename=row.name)

UI_DIR = Path(__file__).resolve().parent.parent / "ui"
if UI_DIR.exists():
    app.mount("/ui", StaticFiles(directory=str(UI_DIR), html=True), name="ui")
