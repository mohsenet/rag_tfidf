import streamlit as st
from io import StringIO
from rag_engine import SimpleRAG

# ===== HANDLE NLTK AVAILABILITY =====
_nltk_available = False
try:
    import nltk
    if nltk.data.find('tokenizers/punkt'):
        _nltk_available = True
    else:
        with st.spinner("Downloading NLTK 'punkt' tokenizer (one-time)..."):
            nltk.download('punkt', quiet=True)
        _nltk_available = True
except Exception:
    _nltk_available = False

# ===== SESSION STATE & UI (rest unchanged) =====

if "document_text" not in st.session_state:
    st.session_state.document_text = None
    st.session_state.document_name = None
if "chunking_choice" not in st.session_state:
    st.session_state.chunking_choice = "fixed"
if "chunk_size" not in st.session_state:
    st.session_state.chunk_size = 10
if "overlap" not in st.session_state:
    st.session_state.overlap = 2

st.set_page_config(page_title="Advanced RAG Demo", layout="centered")
st.title("RAG Question Answering")
st.markdown("Upload a `.txt` file and ask questions about its content.")

uploaded_file = st.file_uploader("Choose a text file (.txt)", type=["txt"])
if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    st.session_state.document_text = stringio.read()
    st.session_state.document_name = uploaded_file.name
    st.success(f"✅ Uploaded: `{uploaded_file.name}`")

document_text = st.session_state.document_text

if document_text is None:
    st.info("👆 Please upload a `.txt` file to begin.")
else:
    st.info(f"📄 Working with: **{st.session_state.document_name}** ({len(document_text)} characters)")

# Sidebar
st.sidebar.header("SplitOptions")
chunking_choice = st.sidebar.selectbox(
    "Chunking Strategy",
    options=["fixed", "regex", "nltk"],
    index=["fixed", "regex", "nltk"].index(st.session_state.chunking_choice)
)
st.session_state.chunking_choice = chunking_choice

if chunking_choice == "fixed":
    chunk_size = st.sidebar.number_input("Chunk Size (words)", 5, 100, st.session_state.chunk_size)
    overlap = st.sidebar.number_input("Overlap (words)", 0, chunk_size - 1, min(st.session_state.overlap, chunk_size - 1))
    st.session_state.chunk_size = chunk_size
    st.session_state.overlap = overlap

if chunking_choice == "nltk" and not _nltk_available:
    st.warning("⚠️ NLTK not available. Install with `pip install nltk`.")

# Build RAG
rag = None
if document_text is not None:
    try:
        rag = SimpleRAG(
            chunking_method=st.session_state.chunking_choice,
            chunk_size=st.session_state.chunk_size,
            overlap=st.session_state.overlap,
            _nltk_available=_nltk_available
        )
        rag.add_documents(document_text)
        st.info(f"✅ Processed into **{len(rag.chunks)} chunks** using **{st.session_state.chunking_choice}** strategy.")
    except Exception as e:
        st.error(f"Error: {e}")

# Query
query = st.text_input("Your question:", placeholder="e.g., What is the main idea?")
if query and rag:
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
elif query and not rag:
    st.warning("Please upload a document first.")

# Sidebar credits
st.sidebar.markdown("---")
st.sidebar.markdown("### Developed by:")
st.sidebar.markdown("**Mohsen Moghimbegloo**")
st.sidebar.markdown("[LinkedIn](https://linkedin.com/in/mohsen-moghimbegloo)")
st.sidebar.markdown("[X (Twitter)](https://x.com/Moghimbegloo)")
st.sidebar.markdown("[YouTube](https://www.youtube.com/@mohsenmoghimbegloo)")