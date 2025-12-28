import streamlit as st


def rag_question_answering():
    """
    Initialize the Streamlit page configuration and apply custom CSS styling.
    This should be called at the very beginning of the main app.
    """
    st.set_page_config(
        page_title="Advanced RAG Demo",
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="🔍"
    )
    
    # Custom CSS for modern styling
    st.markdown("""
        <style>
        /* Main header styling */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .main-header h1 {
            color: white;
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }
        
        .main-header p {
            color: rgba(255, 255, 255, 0.9);
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
        }
        
        /* Card styling */
        .info-card {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            margin: 1rem 0;
        }
        
        /* Metric cards */
        .metric-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #667eea;
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: #666;
            margin-top: 0.5rem;
        }
        
        /* Chunk display */
        .chunk-container {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            border-left: 3px solid #667eea;
        }
        
        .chunk-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }
        
        .chunk-score {
            background: #667eea;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        
        /* Sidebar styling */
        .sidebar-section {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        /* Button styling */
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        /* Upload area */
        .uploadedFile {
            border: 2px dashed #667eea;
            border-radius: 8px;
            padding: 1rem;
        }
        
        /* Progress indicator */
        .progress-text {
            text-align: center;
            color: #667eea;
            font-weight: 600;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🔍 RAG Question Answering System</h1>
            <p>Upload your document and ask intelligent questions powered by retrieval-augmented generation</p>
        </div>
    """, unsafe_allow_html=True)


def render_document_status():
    """
    Display the current document status with metrics.
    Shows upload prompt if no document is loaded, otherwise displays document statistics.
    """
    document_text = st.session_state.get("document_text")
    
    if document_text is None:
        st.markdown("""
            <div class="info-card">
                <h3>📤 Getting Started</h3>
                <p>Upload a <code>.txt</code> file to begin analyzing your document. The system will:</p>
                <ul>
                    <li>Split your document into intelligent chunks</li>
                    <li>Create searchable vectors using TF-IDF</li>
                    <li>Enable semantic question answering</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Create metrics columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(document_text):,}</div>
                    <div class="metric-label">Characters</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            word_count = len(document_text.split())
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{word_count:,}</div>
                    <div class="metric-label">Words</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">✓</div>
                    <div class="metric-label">Ready to Query</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="info-card" style="margin-top: 1rem;">
                <strong>📄 Document:</strong> {st.session_state.get('document_name', 'Unknown')}
            </div>
        """, unsafe_allow_html=True)


def render_chunking_options(nltk_available: bool):
    """
    Render the sidebar UI for chunking strategy selection and parameter configuration.
    
    Args:
        nltk_available: Whether NLTK is available for sentence tokenization
    
    Returns:
        str: The selected chunking strategy
    """
    
    st.sidebar.markdown("## ⚙️ Configuration")
    
    # Chunking strategy section
    st.sidebar.markdown("### 📊 Chunking Strategy")
    
    strategy_descriptions = {
        "fixed": "🔢 Fixed-size chunks with overlap",
        "regex": "📝 Sentence-based (Regex)",
        "nltk": "🎯 Sentence-based (NLTK)",
        "paragraph": "📃 Paragraph-based",
        "sliding": "🔄 Sliding window with overlap",
        "recursive": "🌳 Recursive hierarchical splitting",
        "semantic": "🧠 Semantic similarity-based splitting",
        "hierarchical": "📚 Content-aware hierarchical chunking"
    }
    
    all_strategies = ["fixed", "regex", "nltk", "paragraph", "sliding", "recursive", "semantic", "hierarchical"]
    
    chunking_choice = st.sidebar.selectbox(
        "Select Strategy",
        options=all_strategies,
        format_func=lambda x: strategy_descriptions[x],
        index=all_strategies.index(st.session_state.chunking_choice),
        help="Choose how to split your document into chunks"
    )
    st.session_state.chunking_choice = chunking_choice
    
    # Strategy-specific parameters
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎛️ Parameters")
    
    if chunking_choice == "fixed":
        # Fixed-size chunking parameters
        chunk_size = st.sidebar.slider(
            "Chunk Size (words)",
            min_value=5,
            max_value=100,
            value=st.session_state.chunk_size,
            help="Number of words per chunk"
        )
        overlap = st.sidebar.slider(
            "Overlap (words)",
            min_value=0,
            max_value=chunk_size - 1,
            value=min(st.session_state.overlap, chunk_size - 1),
            help="Words shared between consecutive chunks"
        )
        st.session_state.chunk_size = chunk_size
        st.session_state.overlap = overlap
        
        # Visual feedback
        overlap_percent = (overlap / chunk_size * 100) if chunk_size > 0 else 0
        st.sidebar.progress(overlap / chunk_size if chunk_size > 0 else 0)
        st.sidebar.caption(f"Overlap: {overlap_percent:.1f}%")
    
    elif chunking_choice == "sliding":
        # Sliding window parameters
        window_size = st.sidebar.slider(
            "Window Size (words)",
            min_value=10,
            max_value=100,
            value=st.session_state.window_size,
            help="Number of words in each chunk"
        )
        step_size = st.sidebar.slider(
            "Step Size (words)",
            min_value=1,
            max_value=window_size,
            value=min(st.session_state.step_size, window_size),
            help="How many words to move forward for next chunk"
        )
        st.session_state.window_size = window_size
        st.session_state.step_size = step_size
        
        # Calculate and display overlap
        overlap_words = window_size - step_size
        overlap_percent = (overlap_words / window_size * 100)
        
        st.sidebar.progress(overlap_words / window_size)
        st.sidebar.info(f"""
        **🔄 Overlap Analysis**
        - Overlap: {overlap_words} words ({overlap_percent:.1f}%)
        - Each chunk shares content with neighbors
        """)
    
    elif chunking_choice == "recursive":
        # Recursive chunking parameters
        recursive_chunk_size = st.sidebar.slider(
            "Chunk Size (characters)",
            min_value=100,
            max_value=2000,
            value=st.session_state.recursive_chunk_size,
            step=50,
            help="Target chunk size in characters"
        )
        recursive_overlap = st.sidebar.slider(
            "Overlap (characters)",
            min_value=0,
            max_value=min(500, recursive_chunk_size - 1),
            value=min(st.session_state.recursive_overlap, recursive_chunk_size - 1),
            help="Characters shared between consecutive chunks"
        )
        st.session_state.recursive_chunk_size = recursive_chunk_size
        st.session_state.recursive_overlap = recursive_overlap
        
        overlap_percent = (recursive_overlap / recursive_chunk_size * 100)
        st.sidebar.progress(recursive_overlap / recursive_chunk_size)
        
        st.sidebar.info(f"""
        **🌳 Recursive Splitting**
        - Overlap: {overlap_percent:.1f}%
        - Tries paragraphs → sentences → words
        - Preserves semantic boundaries
        """)
    
    elif chunking_choice == "semantic":
        # Semantic chunking parameters
        semantic_buffer_size = st.sidebar.slider(
            "Buffer Size (sentences)",
            min_value=1,
            max_value=5,
            value=st.session_state.semantic_buffer_size,
            help="Number of sentences to group for comparison"
        )
        semantic_threshold = st.sidebar.slider(
            "Similarity Threshold",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.semantic_threshold,
            step=0.05,
            help="Minimum similarity to keep sentences together (lower = more splits)"
        )
        st.session_state.semantic_buffer_size = semantic_buffer_size
        st.session_state.semantic_threshold = semantic_threshold
        
        st.sidebar.info(f"""
        **🧠 Semantic Chunking**
        - Buffer: {semantic_buffer_size} sentence(s)
        - Threshold: {semantic_threshold:.2f}
        - Splits when similarity drops
        - Creates coherent topic-based chunks
        """)
        
        st.sidebar.markdown("**📊 How it works:**")
        st.sidebar.caption("""
        1. Compares sentence groups
        2. Calculates semantic similarity
        3. Splits when similarity < threshold
        4. Results in naturally coherent chunks
        """)
    
    elif chunking_choice == "hierarchical":
        # Hierarchical chunking parameters
        hierarchical_max_size = st.sidebar.slider(
            "Max Chunk Size (characters)",
            min_value=500,
            max_value=3000,
            value=st.session_state.hierarchical_max_size,
            step=100,
            help="Maximum size for each chunk"
        )
        hierarchical_preserve = st.sidebar.checkbox(
            "Preserve Structure Context",
            value=st.session_state.hierarchical_preserve,
            help="Keep heading context in continuation chunks"
        )
        st.session_state.hierarchical_max_size = hierarchical_max_size
        st.session_state.hierarchical_preserve = hierarchical_preserve
        
        st.sidebar.info(f"""
        **📚 Hierarchical Chunking**
        - Max size: {hierarchical_max_size} chars
        - Structure preservation: {'✓ Enabled' if hierarchical_preserve else '✗ Disabled'}
        - Detects headings, lists, sections
        - Respects document hierarchy
        """)
        
        st.sidebar.markdown("**🔍 Detected Elements:**")
        st.sidebar.caption("""
        • Markdown headings (# ## ###)
        • Underlined headings (===, ---)
        • Title case headings
        • Bullet/numbered lists
        • Paragraph boundaries
        """)
        
        st.sidebar.markdown("**✨ Key Features:**")
        st.sidebar.caption("""
        • Keeps headings with their content
        • Maintains list item grouping
        • Preserves section hierarchy
        • Adds context to continuations
        """)
    
    elif chunking_choice == "paragraph":
        # Paragraph chunking (no parameters)
        st.sidebar.info("""
        **📝 Paragraph Mode**
        - Splits at double newlines
        - Preserves natural structure
        - No additional parameters
        """)
    
    elif chunking_choice in ["regex", "nltk"]:
        # Sentence-based chunking (no parameters)
        st.sidebar.info(f"""
        **{"🎯 NLTK" if chunking_choice == "nltk" else "📝 Regex"} Sentence Mode**
        - Automatic sentence detection
        - Natural language boundaries
        - No additional parameters
        """)
    
    # Warning for NLTK availability
    if chunking_choice == "nltk" and not nltk_available:
        st.sidebar.warning("⚠️ NLTK not available. Install with `pip install nltk`")
    
    return chunking_choice


def render_developer_info():
    """
    Display developer information and social links in the sidebar.
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👨‍💻 Developer")
    
    st.sidebar.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h4 style="margin: 0;">Mohsen Moghimbegloo</h4>
            <p style="color: #666; font-size: 0.9rem; margin: 0.5rem 0;">
                Machine Learning Engineer
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Social links with icons
    col1, col2, col3 = st.sidebar.columns(3)
    
    with col1:
        st.markdown("""
            <a href="https://linkedin.com/in/mohsen-moghimbegloo" target="_blank" 
               style="text-decoration: none; color: #0077b5;">
                <div style="text-align: center; padding: 0.5rem;">
                    <div style="font-size: 1.5rem;">💼</div>
                    <div style="font-size: 0.7rem;">LinkedIn</div>
                </div>
            </a>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <a href="https://x.com/Moghimbegloo" target="_blank" 
               style="text-decoration: none; color: #1DA1F2;">
                <div style="text-align: center; padding: 0.5rem;">
                    <div style="font-size: 1.5rem;">𝕏</div>
                    <div style="font-size: 0.7rem;">Twitter</div>
                </div>
            </a>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <a href="https://www.youtube.com/@mohsenmoghimbegloo" target="_blank" 
               style="text-decoration: none; color: #FF0000;">
                <div style="text-align: center; padding: 0.5rem;">
                    <div style="font-size: 1.5rem;">▶️</div>
                    <div style="font-size: 0.7rem;">YouTube</div>
                </div>
            </a>
        """, unsafe_allow_html=True)


def render_query_results(response: str, results: list):
    """
    Display query results with retrieved chunks and similarity scores.
    
    Args:
        response: The generated response text
        results: List of tuples containing (chunk_text, similarity_score)
    """
    
    # Response section
    st.markdown("### 💡 Answer")
    st.markdown(f"""
        <div class="info-card">
            <p style="font-size: 1.1rem; line-height: 1.6;">{response}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Retrieved chunks section
    st.markdown("### 📚 Retrieved Chunks")
    st.caption("Top relevant passages from the document, ranked by similarity")
    
    for i, (chunk, score) in enumerate(results, 1):
        # Color coding based on score
        if score > 0.5:
            border_color = "#10b981"  # Green
            score_bg = "#10b981"
        elif score > 0.3:
            border_color = "#f59e0b"  # Orange
            score_bg = "#f59e0b"
        else:
            border_color = "#ef4444"  # Red
            score_bg = "#ef4444"
        
        st.markdown(f"""
            <div class="chunk-container" style="border-left-color: {border_color};">
                <div class="chunk-header">
                    <strong>Chunk {i}</strong>
                    <span class="chunk-score" style="background: {score_bg};">
                        {score:.4f}
                    </span>
                </div>
                <p style="margin: 0; color: #333; line-height: 1.6;">{chunk}</p>
            </div>
        """, unsafe_allow_html=True)
        