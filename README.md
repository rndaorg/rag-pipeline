# 1. Create & activate virtual environment
python -m venv venv && source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate                         # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start local LLM (optional but recommended)
ollama pull llama3.2 && ollama serve

# 4. Launch Streamlit
streamlit run app.py