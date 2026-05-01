from sentence_transformers import SentenceTransformer
from config import EMBED_MODEL

_embedder = None

def get_embedder():
    """Lazy-loaded singleton for the embedding model."""
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBED_MODEL)
    return _embedder