import os
import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException
from models.schemas import UploadResponse, DocumentInfo
from services.document_loader import load_document
from services.embedding_service import embed_texts
from services.vector_store import add_chunks, get_stats
from utils.text_splitter import split_text

router = APIRouter()

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 800))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 100))

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md"}


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}. Allowed: pdf, txt, md")

    Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    dest = os.path.join(UPLOAD_DIR, file.filename)

    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        text = load_document(dest)
    except Exception as e:
        os.remove(dest)
        raise HTTPException(status_code=422, detail=f"Failed to extract text: {str(e)}")

    if not text.strip():
        os.remove(dest)
        raise HTTPException(status_code=422, detail="Document appears to be empty or unreadable.")

    chunks = split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
    if not chunks:
        raise HTTPException(status_code=422, detail="No text chunks could be created from this document.")

    embeddings = embed_texts(chunks)
    add_chunks(chunks, embeddings, file.filename)

    return UploadResponse(
        message="Document uploaded and indexed successfully.",
        filename=file.filename,
        chunks_created=len(chunks),
    )


@router.get("/documents", response_model=list[DocumentInfo])
async def list_documents():
    stats = get_stats()
    docs = stats.get("documents", [])
    result = []
    for fname in docs:
        fpath = os.path.join(UPLOAD_DIR, fname)
        size = os.path.getsize(fpath) if os.path.exists(fpath) else 0
        # Count chunks for this doc
        from services.vector_store import _doc_map
        chunks = _doc_map.count(fname)
        result.append(DocumentInfo(filename=fname, size=size, chunks=chunks))
    return result
