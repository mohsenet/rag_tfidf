import streamlit as st

st.set_page_config(page_title="About This App", layout="centered")

st.title("About This App")

st.markdown("""
This application demonstrates a **simple Retrieval-Augmented Generation (RAG) system** built with:

- **TF-IDF vectorization** for text representation  
- **Cosine similarity** for relevance scoring  
- **Fixed-size chunking** of input documents  

The system is designed to answer questions about a provided text document (currently focused on **Maryam Mirzakhani**, the renowned mathematician).

### How It Works
1. The document is split into small chunks.
2. Each chunk is converted into a TF-IDF vector.
3. When you ask a question, the query is vectorized and compared to all chunks.
4. The top-3 most relevant chunks are retrieved and combined into a response.

### Pages
- **Main Page**: Ask questions and get AI-generated answers.
- **View Document**: See the full source text used by the system.
- **This Page**: Learn about the app’s design and purpose.

> **Note**: This is a lightweight, educational implementation—**not a production-grade RAG system**. It uses classical NLP (not embeddings or LLMs).

Built with **Streamlit**, **scikit-learn**, and **NumPy**.
""")

st.markdown("👈 Use the sidebar to navigate back to the main interface.")

# --- Developer Credit in Sidebar (appears on all pages) ---
st.sidebar.markdown("### Developed by:")
st.sidebar.markdown("**Mohsen Moghimbegloo**")
st.sidebar.markdown("[LinkedIn](https://linkedin.com/in/mohsen-moghimbegloo)")
st.sidebar.markdown("[X (Twitter)](https://x.com/Moghimbegloo)")
st.sidebar.markdown("[YouTube](https://www.youtube.com/@mohsenmoghimbegloo)")
