import os
from typing import List, Tuple


def _is_summary_request(question: str) -> bool:
    keywords = [
        "summarize", "summary", "overview", "explain", "describe",
        "what is this document", "what does this document", "tell me about",
        "give me a summary", "whole document", "entire document", "main points",
        "key points", "what is this about", "what is the document about",
        "unit", "chapter", "section", "topic"
    ]
    return any(k in question.lower() for k in keywords)


def _build_system_prompt() -> str:
    return (
        "You are DocuMind, an expert AI document assistant. "
        "Answer questions based strictly on the provided document context. "
        "IMPORTANT: Always follow the user's requested format exactly — "
        "if they ask for 5 points, give exactly 5 points; "
        "if they ask for short, be brief; "
        "if they ask for 10 lines, give exactly 10 lines. "
        "Use bullet points or numbered lists when asked. "
        "Do not add extra sections, introductions, or conclusions unless asked."
    )


def _build_user_prompt(question: str, context_chunks: List[str]) -> str:
    context = "\n\n---\n\n".join(context_chunks)
    context = context[:3000]

    if _is_summary_request(question):
        return (
            f"Based on the following document content, provide a comprehensive, "
            f"detailed summary in 4-5 well-written paragraphs. Cover all major topics, "
            f"key concepts, important details, and conclusions. Be thorough.\n\n"
            f"Document Content:\n{context}\n\n"
            f"Request: {question}"
        )

    return (
        f"Answer the following question in detail using the document context below. "
        f"Provide a thorough response with multiple paragraphs, covering all relevant "
        f"aspects. Include examples and explanations where helpful.\n\n"
        f"Document Context:\n{context}\n\n"
        f"Question: {question}"
    )


def generate_answer_groq(question: str, context_chunks: List[str]) -> str:
    from openai import OpenAI
    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
    )
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    context = "\n\n".join(context_chunks)[:1500]
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": _build_system_prompt()},
            {"role": "user", "content": _build_user_prompt(question, context_chunks)},
        ],
        temperature=0.3,
        max_tokens=800,
    )
    return response.choices[0].message.content.strip()


def run_rag(question: str, top_k: int = 5) -> Tuple[str, List[str]]:
    from services.embedding_service import embed_query
    from services.vector_store import search

    query_vec = embed_query(question)
    fetch_k = 8 if _is_summary_request(question) else top_k
    hits = search(query_vec, top_k=fetch_k)

    if not hits:
        return "No relevant documents found. Please upload documents first.", []

    context_chunks = [chunk for chunk, _, _ in hits]
    sources = [f"[{fname}] {chunk[:200]}..." for chunk, fname, _ in hits]

    answer = generate_answer_groq(question, context_chunks)
    return answer, sources
