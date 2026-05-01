import os
import uuid
import requests
from config import TOP_K, LLM_API_URL, LLM_MODEL, LLM_API_KEY
from models import get_embedder

#tbi
from vector_store import get_collection
from document_processor import extract_pdf_text, chunk_documents

def ingest_pdf(pdf_path):
    """Full pipeline: extract → chunk → embed → upsert to vector DB."""
    embedder = get_embedder()
    collection = get_collection()
    
    pages = extract_pdf_text(pdf_path)
    chunks = chunk_documents(pages)
    if not chunks:
        return 0

    texts = [c["text"] for c in chunks]
    embeddings = embedder.encode(texts, show_progress_bar=False).tolist()
    ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [{"source": c["source"], "page": c["page"]} for c in chunks]

    BATCH = 500
    for i in range(0, len(chunks), BATCH):
        collection.upsert(
            ids=ids[i:i+BATCH],
            embeddings=embeddings[i:i+BATCH],
            metadatas=metadatas[i:i+BATCH],
            documents=texts[i:i+BATCH]
        )
    return len(chunks)

def query_rag(question):
    """Retrieves top-K chunks and generates a cited answer."""
    embedder = get_embedder()
    collection = get_collection()
    
    query_vec = embedder.encode([question]).tolist()[0]
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=TOP_K,
        include=["documents", "metadatas"]
    )

    if not results["documents"][0]:
        return "📭 No relevant context found in uploaded documents.", []

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    context_parts = []
    sources = []
    for i, (doc, meta) in enumerate(zip(docs, metas)):
        tag = f"[{i+1}]"
        context_parts.append(f"{tag} {doc}")
        sources.append({"idx": i+1, "source": meta["source"], "page": meta["page"]})

    prompt = f"""You are an expert analyst. Answer based ONLY on the provided context. 
If the context lacks information, state that clearly. Always cite sources using [1], [2], etc.

Context:
{chr(10).join(context_parts)}

Question: {question}
Answer:"""

    headers = {"Content-Type": "application/json"}
    if LLM_API_KEY:
        headers["Authorization"] = f"Bearer {LLM_API_KEY}"

    try:
        res = requests.post(LLM_API_URL, json={
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        }, headers=headers, timeout=30)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"], sources
    except Exception as e:
        return f"⚠️ LLM Error: {str(e)}", sources