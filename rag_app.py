import streamlit as st
from typing import List, Tuple
import re
from io import StringIO
import nltk

# Optional NLTK
try:
    import nltk
    _nltk_available = True
    if not nltk.data.find('tokenizers/punkt'):
        with st.spinner("Downloading NLTK 'punkt' tokenizer (one-time)..."):
            nltk.download('punkt', quiet=True)
except Exception:
    _nltk_available = False

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


# ===== CHUNKING STRATEGIES =====

def chunk_fixed_size_with_overlap(text: str, size: int = 15, overlap: int = 0) -> List[str]:
    if size <= 0:
        raise ValueError("Chunk size must be > 0")
    if overlap < 0:
        overlap = 0
    if overlap >= size:
        overlap = size - 1
    words = text.split()
    chunks = []
    step = size - overlap
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + size])
        if chunk:
            chunks.append(chunk)
    return chunks


def chunk_sentence_regex(text: str) -> List[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s]


def chunk_sentence_nltk(text: str) -> List[str]:
    if not _nltk_available:
        return chunk_sentence_regex(text)
    return nltk.sent_tokenize(text)


# ===== RAG SYSTEM =====

class SimpleRAG:
    def __init__(self, chunking_method: str = "fixed", chunk_size: int = 15, overlap: int = 0):
        self.chunking_method = chunking_method
        self.chunk_size = chunk_size
        self.overlap = overlap if chunking_method == "fixed" else 0
        self.chunks = []
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.chunk_vectors = None

    def _chunk_text(self, text: str) -> List[str]:
        if self.chunking_method == "fixed":
            return chunk_fixed_size_with_overlap(text, self.chunk_size, self.overlap)
        elif self.chunking_method == "regex":
            return chunk_sentence_regex(text)
        elif self.chunking_method == "nltk":
            return chunk_sentence_nltk(text) if _nltk_available else chunk_sentence_regex(text)
        else:
            raise ValueError(f"Unknown method: {self.chunking_method}")

    def add_documents(self, text: str):
        self.chunks = self._chunk_text(text)
        if not self.chunks:
            raise ValueError("No chunks extracted.")
        self.chunk_vectors = self.vectorizer.fit_transform(self.chunks)

    def search_with_scores(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        if self.chunk_vectors is None or self.chunk_vectors.shape[0] == 0:
            return []
        query_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self.chunk_vectors).flatten()
        top_indices = sims.argsort()[-top_k:][::-1]
        return [(self.chunks[i], float(sims[i])) for i in top_indices]

    def generate_response(self, query: str, top_k=3):
        results = self.search_with_scores(query, top_k)
        if not results:
            return "I don't have enough information to answer that question."
        return f"Based on the information: {' '.join(chunk for chunk, _ in results)}"


# ===== INITIALIZE SESSION STATE =====

if "document_text" not in st.session_state:
    st.session_state.document_text = None
    st.session_state.document_name = None

# Preserve UI controls across reloads
if "chunking_choice" not in st.session_state:
    st.session_state.chunking_choice = "fixed"
if "chunk_size" not in st.session_state:
    st.session_state.chunk_size = 10
if "overlap" not in st.session_state:
    st.session_state.overlap = 2


# ===== STREAMLIT UI =====

st.set_page_config(page_title="Advanced RAG Demo", layout="centered")
st.title("RAG Question Answering")
st.markdown("Upload a `.txt` file and ask questions about its content.")

# === FILE UPLOAD (updates session state) ===
uploaded_file = st.file_uploader("Choose a text file (.txt)", type=["txt"])

if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    st.session_state.document_text = stringio.read()
    st.session_state.document_name = uploaded_file.name
    st.success(f"✅ Uploaded: `{uploaded_file.name}`")

# === WORK WITH SESSION STATE DOCUMENT ===
document_text = st.session_state.document_text

if document_text is None:
    st.info("👆 Please upload a `.txt` file to begin.")
    # Do NOT st.stop() — allow sidebar interaction and state updates
else:
    st.info(f"📄 Working with: **{st.session_state.document_name}** ({len(document_text)} characters)")

# === SIDEBAR CONTROLS (sync with session state) ===
st.sidebar.header("SplitOptions")

chunking_choice = st.sidebar.selectbox(
    "Chunking Strategy",
    options=["fixed", "regex", "nltk"],
    index=["fixed", "regex", "nltk"].index(st.session_state.chunking_choice),
    key="chunking_selector"  # optional, but helps clarity
)

# Update session state when user changes selection
st.session_state.chunking_choice = chunking_choice

chunk_size = 10
overlap = 0

if chunking_choice == "fixed":
    chunk_size = st.sidebar.number_input(
        "Chunk Size (words)",
        min_value=5,
        max_value=100,
        value=st.session_state.chunk_size,
        key="chunk_size_input"
    )
    overlap = st.sidebar.number_input(
        "Overlap (words)",
        min_value=0,
        max_value=chunk_size - 1,
        value=min(st.session_state.overlap, chunk_size - 1),
        key="overlap_input"
    )
    st.session_state.chunk_size = chunk_size
    st.session_state.overlap = overlap

if chunking_choice == "nltk" and not _nltk_available:
    st.warning("⚠️ NLTK not available. Install with `pip install nltk`.")

# === BUILD RAG ONLY IF DOCUMENT EXISTS ===
rag = None
if document_text is not None:
    try:
        rag = SimpleRAG(
            chunking_method=st.session_state.chunking_choice,
            chunk_size=st.session_state.chunk_size,
            overlap=st.session_state.overlap
        )
        rag.add_documents(document_text)
        st.info(f"✅ Processed into **{len(rag.chunks)} chunks** using **{st.session_state.chunking_choice}** strategy.")
    except Exception as e:
        st.error(f"Error initializing RAG: {e}")

# === QUERY INPUT ===
query = st.text_input("Your question:", placeholder="e.g., What is the main idea?")

if query and rag is not None:
    with st.spinner("Searching..."):
        response = rag.generate_response(query)
        results = rag.search_with_scores(query, top_k=3)

    st.subheader("Response")
    st.write(response)

    st.subheader("Retrieved Chunks with Similarity Scores")
    for i, (chunk, score) in enumerate(results, 1):
        st.markdown(f"**Chunk {i}** (`similarity = {score:.4f}`)")
        st.text(chunk)
        st.divider()
elif query and rag is None:
    st.warning("Please upload a document first.")

# === SIDEBAR CREDITS ===
st.sidebar.markdown("---")
st.sidebar.markdown("### Developed by:")
st.sidebar.markdown("**Mohsen Moghimbegloo**")
st.sidebar.markdown("[LinkedIn](https://linkedin.com/in/mohsen-moghimbegloo)")
st.sidebar.markdown("[X (Twitter)](https://x.com/Moghimbegloo)")
st.sidebar.markdown("[YouTube](https://www.youtube.com/@mohsenmoghimbegloo)")
