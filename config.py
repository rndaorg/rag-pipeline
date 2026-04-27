import os

# Embedding & Vector DB
EMBED_MODEL = "all-MiniLM-L6-v2"
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "pdf_rag"
TOP_K = 3

# Chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# LLM (defaults, override via env vars)
LLM_API_URL = os.getenv("LLM_API_URL", "http://localhost:11434/v1/chat/completions")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")
LLM_API_KEY = os.getenv("LLM_API_KEY")