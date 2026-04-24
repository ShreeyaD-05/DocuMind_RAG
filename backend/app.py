import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import HealthResponse
from services.vector_store import get_stats, clear
from routes.upload import router as upload_router
from routes.query import router as query_router

app = FastAPI(title="DocuMind RAG API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(query_router)


@app.get("/health", response_model=HealthResponse)
async def health():
    stats = get_stats()
    return HealthResponse(
        status="ok",
        documents_loaded=len(stats.get("documents", [])),
        index_size=stats.get("index_size", 0),
    )


@app.delete("/clear")
async def clear_index():
    """Remove all indexed documents."""
    clear()
    # Delete contents but keep the directory (volume mount can't be removed)
    upload_dir = os.getenv("UPLOAD_DIR", "./uploads")
    if os.path.exists(upload_dir):
        for item in os.listdir(upload_dir):
            item_path = os.path.join(upload_dir, item)
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    import shutil
                    shutil.rmtree(item_path)
            except Exception:
                pass
    return {"message": "All documents cleared."}
