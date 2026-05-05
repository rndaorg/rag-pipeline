import os
from pypdf import PdfReader
from config import CHUNK_SIZE, CHUNK_OVERLAP

def extract_pdf_text(pdf_path):
    """Extracts text and page numbers from a PDF."""
    reader = PdfReader(pdf_path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text.strip():
            pages.append({
                "text": text,
                "page": i + 1,
                "source": os.path.basename(pdf_path)
            })
    return pages

def chunk_documents(pages):
    """Splits pages into overlapping word-based chunks."""
    chunks = []
    for page in pages:
        words = page["text"].split()
        current_chunk = []
        current_len = 0
        
        for word in words:
            current_chunk.append(word)
            current_len += len(word) + 1
            if current_len >= CHUNK_SIZE:
                chunks.append({
                    "text": " ".join(current_chunk),
                    "source": page["source"],
                    "page": page["page"]
                })
                # Build overlap
                overlap = []
                overlap_len = 0
                for w in reversed(current_chunk):
                    if overlap_len + len(w) + 1 > CHUNK_OVERLAP:
                        break
                    overlap.insert(0, w)
                    overlap_len += len(w) + 1
                current_chunk = overlap
                current_len = overlap_len
                
        if current_chunk:
            chunks.append({
                "text": " ".join(current_chunk),
                "source": page["source"],
                "page": page["page"]
            })
    return chunks