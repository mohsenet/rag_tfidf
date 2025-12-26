import streamlit as st
from utils import ensure_nltk_punkt
from ui_components import (
    render_developer_info, 
    rag_question_answering, 
    render_chunking_options, 
    render_document_status
)
from session import init_session_state, handle_uploaded_file
from query_handler import handle_query_interface
from rag_builder import build_rag_engine


# ===== INITIALIZE SESSION STATE FIRST =====
init_session_state()

# ===== HANDLE NLTK AVAILABILITY =====
_nltk_available = ensure_nltk_punkt()

# ===== UI =====
rag_question_answering()

# Create main layout with columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📤 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a text file (.txt)",
        type=["txt"],
        help="Upload a text document to analyze"
    )
    handle_uploaded_file(uploaded_file)

with col2:
    # Show quick stats or instructions
    if st.session_state.document_text:
        st.markdown("### ✅ Document Status")
        st.success("Document loaded successfully!")
        if st.button("🔄 Clear Document", use_container_width=True):
            st.session_state.document_text = None
            st.session_state.document_name = None
            st.rerun()
    else:
        st.markdown("### ℹ️ Quick Start")
        st.info("Upload a document to begin")

# Render document status with metrics
render_document_status()

# Render chunking options in sidebar
chunking_choice = render_chunking_options(_nltk_available)

# Build RAG with visual feedback
if st.session_state.document_text:
    with st.spinner("🔧 Building RAG engine..."):
        rag = build_rag_engine(
            document_text=st.session_state.document_text,
            chunking_choice=st.session_state.chunking_choice,
            chunk_size=st.session_state.chunk_size,
            overlap=st.session_state.overlap,
            window_size=st.session_state.window_size,
            step_size=st.session_state.step_size,
            recursive_chunk_size=st.session_state.recursive_chunk_size,
            recursive_overlap=st.session_state.recursive_overlap,
            nltk_available=_nltk_available
        )
else:
    rag = None

# Add divider
st.markdown("---")

# Query interface
if rag:
    handle_query_interface(rag)
else:
    st.info("👆 Upload a document above to start asking questions")

# --- Developer Credit in Sidebar ---
render_developer_info()

# Add footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Built with ❤️ using Streamlit | 
        <a href="https://github.com" style="color: #667eea;">GitHub</a> | 
        <a href="https://docs.streamlit.io" style="color: #667eea;">Documentation</a></p>
    </div>
""", unsafe_allow_html=True)
