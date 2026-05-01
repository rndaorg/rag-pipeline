import os
import streamlit as st
from rag_engine import ingest_pdf, query_rag
import chromadb
from config import CHROMA_PATH, COLLECTION_NAME

st.set_page_config(page_title="📄 RAG Demo", layout="centered")
st.title("Retrieval-Augmented Generation Pipeline")
st.caption("Upload PDFs → Embed → Retrieve → Generate with Citations")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("⚙️ Settings")
    st.text_input("LLM API URL", value=os.getenv("LLM_API_URL", "http://localhost:11434/v1/chat/completions"), key="api_url")
    st.text_input("LLM Model", value=os.getenv("LLM_MODEL", "llama3.2"), key="llm_model")
    st.text_input("API Key (optional)", type="password", key="api_key")
    
    if st.button("🗑️ Clear Vector DB"):
        try:
            client = chromadb.PersistentClient(path=CHROMA_PATH)
            client.delete_collection(COLLECTION_NAME)
            st.session_state.messages = []
            st.success("✅ Vector database cleared.")
        except Exception:
            st.warning("⚠️ Collection not found or already cleared.")
        st.rerun()

uploaded = st.file_uploader("📎 Upload PDF", type="pdf")
if uploaded:
    tmp_path = f"./tmp_{uploaded.name}"
    with open(tmp_path, "wb") as f:
        f.write(uploaded.getbuffer())
    with st.spinner("📥 Extracting, chunking & embedding..."):
        count = ingest_pdf(tmp_path)
    os.remove(tmp_path)
    st.success(f"✅ Ingested {count} chunks into ChromaDB.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg and msg["sources"]:
            with st.expander("📖 Sources"):
                for s in msg["sources"]:
                    st.markdown(f"**[{s['idx']}]** `{s['source']}` (Page {s['page']})")

if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Retrieving & generating..."):
            ans, srcs = query_rag(prompt)
        st.markdown(ans)
        if srcs:
            with st.expander("📖 Sources"):
                for s in srcs:
                    st.markdown(f"**[{s['idx']}]** `{s['source']}` (Page {s['page']})")
        st.session_state.messages.append({"role": "assistant", "content": ans, "sources": srcs})