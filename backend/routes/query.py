from fastapi import APIRouter, HTTPException
from models.schemas import QueryRequest, QueryResponse
from services.rag_pipeline import run_rag

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    answer, sources = run_rag(request.question, top_k=request.top_k or 5)
    return QueryResponse(answer=answer, sources=sources)
