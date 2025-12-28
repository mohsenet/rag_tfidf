import streamlit as st
from rag_engine import SimpleRAG


def build_rag_engine(document_text: str | None, chunking_choice: str, chunk_size: int, 
                    overlap: int, window_size: int, step_size: int, 
                    recursive_chunk_size: int, recursive_overlap: int,
                    semantic_buffer_size: int, semantic_threshold: float,
                    hierarchical_max_size: int, hierarchical_preserve: bool,
                    nltk_available: bool):
    """
    Builds and initializes a SimpleRAG instance from the provided document text and settings.
    Returns the RAG object or None if document is missing.
    
    Args:
        document_text: The text content to process
        chunking_choice: Selected chunking strategy
        chunk_size: Size for fixed-size chunking (words)
        overlap: Overlap for fixed-size chunking (words)
        window_size: Window size for sliding window chunking (words)
        step_size: Step size for sliding window chunking (words)
        recursive_chunk_size: Target chunk size for recursive chunking (characters)
        recursive_overlap: Overlap for recursive chunking (characters)
        semantic_buffer_size: Buffer size for semantic chunking (sentences)
        semantic_threshold: Similarity threshold for semantic chunking (0-1)
        hierarchical_max_size: Maximum chunk size for hierarchical chunking (characters)
        hierarchical_preserve: Whether to preserve structure context in hierarchical chunking
        nltk_available: Whether NLTK is available for sentence tokenization
    
    Returns:
        SimpleRAG instance or None if document_text is None
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
            hierarchical_max_size=hierarchical_max_size,
            hierarchical_preserve=hierarchical_preserve,
            _nltk_available=nltk_available
        )
        rag.add_documents(document_text)
        
        # Display success message with chunk count
        st.info(f"✅ Processed into **{len(rag.chunks)} chunks** using **{chunking_choice}** strategy.")
        
        return rag
        
    except Exception as e:
        st.error(f"❌ Error building RAG engine: {str(e)}")
        return None
    