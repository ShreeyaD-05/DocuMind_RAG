import os
import json
import pickle
from pathlib import Path
from typing import List, Tuple

import numpy as np
import faiss

INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "./faiss_index")
METADATA_FILE = os.path.join(INDEX_PATH, "metadata.pkl")
INDEX_FILE = os.path.join(INDEX_PATH, "index.faiss")

# In-memory state
_index: faiss.Index = None
_chunks: List[str] = []
_doc_map: List[str] = []  # filename per chunk


def _ensure_dir():
    Path(INDEX_PATH).mkdir(parents=True, exist_ok=True)


def _load_or_create(dim: int = 384) -> faiss.Index:
    global _index, _chunks, _doc_map
    _ensure_dir()
    if os.path.exists(INDEX_FILE) and os.path.exists(METADATA_FILE):
        _index = faiss.read_index(INDEX_FILE)
        with open(METADATA_FILE, "rb") as f:
            data = pickle.load(f)
            _chunks = data["chunks"]
            _doc_map = data["doc_map"]
    else:
        _index = faiss.IndexFlatL2(dim)
        _chunks = []
        _doc_map = []
    return _index


def _save():
    _ensure_dir()
    faiss.write_index(_index, INDEX_FILE)
    with open(METADATA_FILE, "wb") as f:
        pickle.dump({"chunks": _chunks, "doc_map": _doc_map}, f)


def add_chunks(chunks: List[str], embeddings: np.ndarray, filename: str):
    global _index, _chunks, _doc_map
    if _index is None:
        _load_or_create(dim=embeddings.shape[1])
    _index.add(embeddings)
    _chunks.extend(chunks)
    _doc_map.extend([filename] * len(chunks))
    _save()


def search(query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[str, str, float]]:
    """Returns list of (chunk_text, filename, distance)."""
    global _index, _chunks, _doc_map
    if _index is None:
        _load_or_create()
    if _index.ntotal == 0:
        return []
    q = query_embedding.reshape(1, -1)
    distances, indices = _index.search(q, min(top_k, _index.ntotal))
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx >= 0:
            results.append((_chunks[idx], _doc_map[idx], float(dist)))
    return results


def get_stats() -> dict:
    global _index, _chunks, _doc_map
    if _index is None:
        _load_or_create()
    docs = list(set(_doc_map))
    return {
        "index_size": _index.ntotal if _index else 0,
        "documents": docs,
        "total_chunks": len(_chunks),
    }


def clear():
    global _index, _chunks, _doc_map
    _index = faiss.IndexFlatL2(384)
    _chunks = []
    _doc_map = []
    _save()


# Eagerly load on import
_load_or_create()
