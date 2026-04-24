import os
from typing import List
import numpy as np

_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        _model = SentenceTransformer(model_name)
    return _model


def embed_texts(texts: List[str]) -> np.ndarray:
    """Return a 2-D float32 numpy array of embeddings."""
    model = _get_model()
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    return embeddings.astype("float32")


def embed_query(query: str) -> np.ndarray:
    """Return a 1-D float32 numpy array for a single query."""
    return embed_texts([query])[0]
