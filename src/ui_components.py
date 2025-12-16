import streamlit as st


def rag_question_answering():
    st.set_page_config(page_title="Advanced RAG Demo", layout="centered")
    st.title("RAG Question Answering")
    st.markdown("Upload a `.txt` file and ask questions about its content.")


def render_document_status():
    document_text = st.session_state.get("document_text")
    if document_text is None:
        st.info("👆 Please upload a `.txt` file to begin.")
    else:
        st.info(f"📄 Working with: **{st.session_state.get('document_name', 'Unknown')}** ({len(document_text)} characters)")


def render_chunking_options(nltk_available: bool):
    """
    Renders sidebar UI for chunking strategy selection and updates session state.
    Returns the current chunking choice (for convenience, if needed).
    """
    st.sidebar.header("SplitOptions")
    chunking_choice = st.sidebar.selectbox(
        "Chunking Strategy",
        options=["fixed", "regex", "nltk"],
        index=["fixed", "regex", "nltk"].index(st.session_state.chunking_choice)
    )
    st.session_state.chunking_choice = chunking_choice

    if chunking_choice == "fixed":
        chunk_size = st.sidebar.number_input(
            "Chunk Size (words)", 5, 100, value=st.session_state.chunk_size
        )
        overlap = st.sidebar.number_input(
            "Overlap (words)", 0, chunk_size - 1,
            value=min(st.session_state.overlap, chunk_size - 1)
        )
        st.session_state.chunk_size = chunk_size
        st.session_state.overlap = overlap

    if chunking_choice == "nltk" and not nltk_available:
        st.warning("⚠️ NLTK not available. Install with `pip install nltk`.")

    return chunking_choice


def render_developer_info():
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Developed by:")
    st.sidebar.markdown("**Mohsen Moghimbegloo**")
    st.sidebar.markdown("[LinkedIn](https://linkedin.com/in/mohsen-moghimbegloo)")
    st.sidebar.markdown("[X (Twitter)](https://x.com/Moghimbegloo)")
    st.sidebar.markdown("[YouTube](https://www.youtube.com/@mohsenmoghimbegloo)")