import streamlit as st
from utils import ensure_nltk_punkt
from ui_components import render_developer_info, rag_question_answering, render_chunking_options, render_document_status
from session import init_session_state, handle_uploaded_file
from query_handler import handle_query_interface
from rag_builder import build_rag_engine


# ===== INITIALIZE SESSION STATE FIRST =====
init_session_state()

# ===== HANDLE NLTK AVAILABILITY =====
_nltk_available = ensure_nltk_punkt()

# ===== UI =====
rag_question_answering()

uploaded_file = st.file_uploader("Choose a text file (.txt)", type=["txt"])
handle_uploaded_file(uploaded_file) 

render_document_status()

# Render chunking options in sidebar
chunking_choice = render_chunking_options(_nltk_available)

# Build RAG
rag = build_rag_engine(
    document_text=st.session_state.document_text,
    chunking_choice=st.session_state.chunking_choice,
    chunk_size=st.session_state.chunk_size,
    overlap=st.session_state.overlap,
    window_size=st.session_state.window_size,
    step_size=st.session_state.step_size,
    nltk_available=_nltk_available
)

# Query
handle_query_interface(rag)

# --- Developer Credit in Sidebar ---
render_developer_info()
