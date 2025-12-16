# query_handler.py

import streamlit as st
from rag_engine import SimpleRAG


def handle_query_interface(rag: SimpleRAG | None):
    """
    Render the query input and display RAG results.
    """
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

