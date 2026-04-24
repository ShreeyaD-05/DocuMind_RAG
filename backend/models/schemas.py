from pydantic import BaseModel
from typing import List, Optional


class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 5


class QueryResponse(BaseModel):
    answer: str
    sources: List[str]


class DocumentInfo(BaseModel):
    filename: str
    size: int
    chunks: int


class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks_created: int


class HealthResponse(BaseModel):
    status: str
    documents_loaded: int
    index_size: int
