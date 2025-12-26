import streamlit as st
from ui_components import render_developer_info


st.set_page_config(
    page_title="View Document", 
    layout="wide",
    page_icon="📄"
)

# Custom CSS
st.markdown("""
    <style>
    .document-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .document-stats {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .stat-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .stat-item:last-child {
        border-bottom: none;
    }
    
    .stat-label {
        color: #666;
        font-weight: 600;
    }
    
    .stat-value {
        color: #667eea;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="document-header">
        <h1 style="color: white; margin: 0;">📄 Document Viewer</h1>
        <p style="color: rgba(255, 255, 255, 0.9); margin: 0.5rem 0 0 0;">
            View and analyze the complete source document
        </p>
    </div>
""", unsafe_allow_html=True)

# Get document from session state
document_text = st.session_state.get("document_text", None)
document_name = st.session_state.get("document_name", "Uploaded Document")

if document_text is not None:
    # Create two columns for stats and actions
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Calculate stats outside f-string
        char_count = len(document_text)
        word_count = len(document_text.split())
        line_count = len(document_text.splitlines())
        para_count = len([p for p in document_text.split('\n\n') if p.strip()])
        
        st.markdown(f"""
            <div class="document-stats">
                <h3 style="margin-top: 0;">📊 Document Statistics</h3>
                <div class="stat-item">
                    <span class="stat-label">📝 Document Name:</span>
                    <span class="stat-value">{document_name}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">🔤 Total Characters:</span>
                    <span class="stat-value">{char_count:,}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">📖 Total Words:</span>
                    <span class="stat-value">{word_count:,}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">📄 Total Lines:</span>
                    <span class="stat-value">{line_count:,}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">📐 Paragraphs:</span>
                    <span class="stat-value">{para_count:,}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="document-stats">
                <h3 style="margin-top: 0;">⚡ Quick Actions</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Download button
        st.download_button(
            label="📥 Download Document",
            data=document_text,
            file_name=document_name,
            mime="text/plain",
            use_container_width=True
        )
        
        # Copy to clipboard (simulated with text area)
        if st.button("📋 Select All Text", use_container_width=True):
            st.info("Use Ctrl+A (or Cmd+A) and Ctrl+C (or Cmd+C) in the text area below to copy")
        
        # Word frequency analysis
        if st.button("📊 Show Word Frequency", use_container_width=True):
            from collections import Counter
            import re
            
            # Simple word tokenization
            words = re.findall(r'\b\w+\b', document_text.lower())
            word_freq = Counter(words)
            
            # Get top 10 most common words
            st.markdown("### 🔝 Top 10 Most Common Words")
            for word, count in word_freq.most_common(10):
                st.write(f"**{word}**: {count} times")
    
    # Main document display
    st.markdown("---")
    st.markdown("### 📖 Full Document Content")
    
    # Add tabs for different views
    tab1, tab2, tab3 = st.tabs(["📝 Full Text", "📄 Line by Line", "📐 Paragraph View"])
    
    with tab1:
        st.text_area(
            f"Content of '{document_name}':",
            document_text,
            height=600,
            label_visibility="collapsed"
        )
    
    with tab2:
        lines = document_text.splitlines()
        st.markdown(f"*Total lines: {len(lines)}*")
        for i, line in enumerate(lines, 1):
            if line.strip():  # Only show non-empty lines
                st.markdown(f"**Line {i}:** {line}")
    
    with tab3:
        paragraphs = [p.strip() for p in document_text.split('\n\n') if p.strip()]
        st.markdown(f"*Total paragraphs: {len(paragraphs)}*")
        for i, para in enumerate(paragraphs, 1):
            with st.expander(f"Paragraph {i} ({len(para.split())} words)"):
                st.write(para)
    
    # Additional analysis
    st.markdown("---")
    st.markdown("### 🔍 Document Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_word_length = sum(len(word) for word in document_text.split()) / len(document_text.split())
        st.metric("Average Word Length", f"{avg_word_length:.2f} chars")
    
    with col2:
        sentences = len([s for s in document_text.split('.') if s.strip()])
        st.metric("Estimated Sentences", sentences)
    
    with col3:
        avg_words_per_sentence = len(document_text.split()) / max(sentences, 1)
        st.metric("Avg Words/Sentence", f"{avg_words_per_sentence:.1f}")

else:
    # No document loaded
    st.markdown("""
        <div class="document-stats" style="text-align: center; padding: 3rem;">
            <h3>📭 No Document Loaded</h3>
            <p style="color: #666; margin: 1rem 0;">
                Please upload a <code>.txt</code> file on the main RAG page to view its contents here.
            </p>
            <p style="color: #666;">
                Once uploaded, you'll be able to view the full document, see statistics, 
                and perform various analyses.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Tip:** Use the sidebar to navigate to the main RAG page and upload your document.")

# Navigation hint
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 1rem; background: #f9fafb; border-radius: 8px;">
        <p style="margin: 0; color: #666;">
            👈 Use the sidebar to navigate between pages
        </p>
    </div>
""", unsafe_allow_html=True)

# --- Developer Credit in Sidebar ---
render_developer_info()