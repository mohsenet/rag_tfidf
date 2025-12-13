import streamlit as st
from io import StringIO


def init_session_state():
    """Initialize default values in st.session_state if not already set."""
    if "document_text" not in st.session_state:
        st.session_state.document_text = None
        st.session_state.document_name = None

    if "chunking_choice" not in st.session_state:
        st.session_state.chunking_choice = "fixed"

    if "chunk_size" not in st.session_state:
        st.session_state.chunk_size = 10

    if "overlap" not in st.session_state:
        st.session_state.overlap = 2

def handle_uploaded_file(uploaded_file):
    """Process an uploaded file and update session state."""
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.session_state.document_text = stringio.read()
        st.session_state.document_name = uploaded_file.name
        st.success(f"✅ Uploaded: `{uploaded_file.name}`")
        