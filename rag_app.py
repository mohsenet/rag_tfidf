import streamlit as st
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import os

def chunk_fixed_size(text: str, size: int = 15) -> List[str]:
    words = text.split()
    return [" ".join(words[i:i + size]) for i in range(0, len(words), size)]

class SimpleRAG:
    def __init__(self):
        self.chunks = []
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.chunk_vectors = None

    def add_documents(self, text: str, chunk_size: int = 15):
        self.chunks = chunk_fixed_size(text, chunk_size)
        self.chunk_vectors = self.vectorizer.fit_transform(self.chunks)

    def search(self, query: str, top_k: int = 3) -> List[str]:
        if self.chunk_vectors is None:
            return []
        query_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self.chunk_vectors).flatten()
        top_idx = sims.argsort()[-top_k:][::-1]
        return [self.chunks[i] for i in top_idx]

    def generate_response(self, query: str, top_k=3):
        chunks = self.search(query, top_k)
        if not chunks:
            return "I don't have enough information to answer that question."
        return f"Based on the information: {' '.join(chunks)}"

# Load RAG once
@st.cache_resource
def get_rag():
    path = "./content.txt"
    if not os.path.exists(path):
        st.error("Document not found!")
        return None
    with open(path, encoding="utf-8") as f:
        text = f.read()
    rag = SimpleRAG()
    rag.add_documents(text, chunk_size=10)
    return rag

# --- UI ---
st.set_page_config(page_title="RAG Demo", layout="centered")
st.title("RAG Question Answering")
st.markdown("Ask questions about Maryam Mirzakhani.")

rag = get_rag()
if not rag:
    st.stop()

query = st.text_input("Your question:", placeholder="What medal did she receive?")
if query:
    with st.spinner("Searching..."):
        response = rag.generate_response(query)
        chunks = rag.search(query, top_k=3)
    
    st.subheader("Response")
    st.write(response)
    
    with st.expander("🔍 Retrieved Chunks"):
        for i, c in enumerate(chunks, 1):
            st.write(f"**{i}.** {c}")

# --- Developer Credit in Sidebar (appears on all pages) ---
st.sidebar.markdown("### Developed by:")
st.sidebar.markdown("**Mohsen Moghimbegloo**")
st.sidebar.markdown("[LinkedIn](https://linkedin.com/in/mohsen-moghimbegloo)")
st.sidebar.markdown("[X (Twitter)](https://x.com/Moghimbegloo)")
st.sidebar.markdown("[YouTube](https://www.youtube.com/@mohsenmoghimbegloo)")
