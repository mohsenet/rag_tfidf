import streamlit as st
from rag_engine import SimpleRAG


def build_rag_engine(document_text: str | None, chunking_choice: str, chunk_size: int, 
                    overlap: int, window_size: int, step_size: int, 
                    recursive_chunk_size: int, recursive_overlap: int,
                    semantic_buffer_size: int, semantic_threshold: float,
                    nltk_available: bool):
    """
    Builds and initializes a SimpleRAG instance from the provided document text and settings.
    Returns the RAG object or None if document is missing.
    """
    if document_text is None:
        return None

    try:
        rag = SimpleRAG(
            chunking_method=chunking_choice,
            chunk_size=chunk_size,
            overlap=overlap,
            window_size=window_size,
            step_size=step_size,
            recursive_chunk_size=recursive_chunk_size,
            recursive_overlap=recursive_overlap,
            semantic_buffer_size=semantic_buffer_size,
            semantic_threshold=semantic_threshold,
            _nltk_available=nltk_available
        )
        rag.add_documents(document_text)
        st.info(f"✅ Processed into **{len(rag.chunks)} chunks** using **{chunking_choice}** strategy.")
        return rag
    except Exception as e:
        st.error(f"Error: {e}")
        return None
    