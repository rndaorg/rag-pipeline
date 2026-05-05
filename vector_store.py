import chromadb
from config import CHROMA_PATH, COLLECTION_NAME

_collection = None

def get_collection():
    """Returns or creates the ChromaDB collection."""
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        try:
            _collection = client.get_collection(name=COLLECTION_NAME)
        except ValueError:
            _collection = client.create_collection(
                name=COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
    return _collection