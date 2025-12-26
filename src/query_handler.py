import streamlit as st
from rag_engine import SimpleRAG
from ui_components import render_query_results


def handle_query_interface(rag: SimpleRAG | None):
    """
    Enhanced query interface with better UX and visual feedback.
    """
    
    st.markdown("### 🤔 Ask a Question")
    
    # Create columns for query input and button
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "Your question:",
            placeholder="e.g., What is the main idea? Who won the Fields Medal?",
            label_visibility="collapsed"
        )
    
    with col2:
        search_button = st.button("🔍 Search", use_container_width=True)
    
    # Add example questions
    if not query:
        st.markdown("#### 💭 Example Questions")
        example_questions = [
            "What is the main topic of this document?",
            "Who is the main person discussed?",
            "What are the key achievements mentioned?",
            "When did important events occur?",
        ]
        
        cols = st.columns(2)
        for idx, eq in enumerate(example_questions):
            with cols[idx % 2]:
                if st.button(f"💡 {eq}", key=f"example_{idx}", use_container_width=True):
                    query = eq
                    st.rerun()
    
    # Process query
    if (query and rag) or (search_button and query and rag):
        with st.spinner("🔎 Searching through document chunks..."):
            try:
                response = rag.generate_response(query)
                results = rag.search_with_scores(query, top_k=3)
                
                # Display results using enhanced UI
                render_query_results(response, results)
                
                # Add download option for results
                st.markdown("---")
                result_text = f"Query: {query}\n\nResponse: {response}\n\n"
                result_text += "Retrieved Chunks:\n"
                for i, (chunk, score) in enumerate(results, 1):
                    result_text += f"\nChunk {i} (score: {score:.4f}):\n{chunk}\n"
                
                st.download_button(
                    label="📥 Download Results",
                    data=result_text,
                    file_name="rag_results.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
    
    elif query and not rag:
        st.warning("⚠️ Please upload a document first before asking questions.")
    
    # Add helpful tips
    with st.expander("💡 Tips for Better Results"):
        st.markdown("""
        **How to get the best answers:**
        
        1. **Be Specific**: Instead of "Tell me about this", ask "What are the main achievements discussed?"
        2. **Use Keywords**: Include important terms from your document
        3. **Try Different Phrasings**: If you don't get good results, rephrase your question
        4. **Check Similarity Scores**: Scores above 0.5 generally indicate relevant chunks
        5. **Experiment with Chunking**: Different strategies work better for different document types
        
        **Understanding Similarity Scores:**
        - 🟢 **> 0.5**: Highly relevant
        - 🟡 **0.3 - 0.5**: Moderately relevant
        - 🔴 **< 0.3**: Low relevance
        """)
        