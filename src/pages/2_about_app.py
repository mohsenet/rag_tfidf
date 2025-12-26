import streamlit as st
from ui_components import render_developer_info


st.set_page_config(
    page_title="About This App", 
    layout="wide",
    page_icon="ℹ️"
)

# Custom CSS for about page
st.markdown("""
    <style>
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-top: 4px solid #667eea;
    }
    
    .tech-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .comparison-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    
    .comparison-table th {
        background: #667eea;
        color: white;
        padding: 1rem;
        text-align: left;
    }
    
    .comparison-table td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .comparison-table tr:nth-child(even) {
        background: #f9fafb;
    }
    </style>
""", unsafe_allow_html=True)

# Hero section
st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 3rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0;">ℹ️ About This Application</h1>
        <p style="color: rgba(255, 255, 255, 0.9); font-size: 1.2rem; margin: 1rem 0 0 0;">
            A comprehensive educational implementation of Retrieval-Augmented Generation
        </p>
    </div>
""", unsafe_allow_html=True)

# Two column layout for overview
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
        <div class="feature-card">
            <h3>🎯 What is This Application?</h3>
            <p style="line-height: 1.8;">
                This application demonstrates a <strong>Retrieval-Augmented Generation (RAG)</strong> 
                system using classical NLP techniques. It enables intelligent question-answering over 
                text documents by combining information retrieval with response generation.
            </p>
            <p style="line-height: 1.8;">
                Currently configured with biographical information about <strong>Maryam Mirzakhani</strong>, 
                the groundbreaking mathematician who became the first woman to win the Fields Medal.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <h3>📊 Key Statistics</h3>
            <ul style="list-style: none; padding: 0;">
                <li>🔢 <strong>5</strong> Chunking Strategies</li>
                <li>📝 <strong>TF-IDF</strong> Vectorization</li>
                <li>🎯 <strong>Cosine</strong> Similarity</li>
                <li>⚡ <strong>Real-time</strong> Processing</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Core components section
st.markdown("## 🔧 Core Components")

components = [
    {
        "icon": "📄",
        "title": "Text Chunking",
        "description": "Intelligently divides documents into manageable pieces using various strategies optimized for different document types and use cases."
    },
    {
        "icon": "🔢",
        "title": "TF-IDF Vectorization",
        "description": "Converts text into numerical vectors that capture term importance, enabling mathematical comparison of semantic similarity."
    },
    {
        "icon": "📐",
        "title": "Cosine Similarity",
        "description": "Measures the angle between query and document vectors to determine relevance, providing scores from 0 (unrelated) to 1 (identical)."
    },
    {
        "icon": "💡",
        "title": "Response Synthesis",
        "description": "Combines the most relevant chunks into coherent answers, providing context-aware responses to user queries."
    }
]

cols = st.columns(2)
for idx, comp in enumerate(components):
    with cols[idx % 2]:
        st.markdown(f"""
            <div class="feature-card">
                <h3>{comp['icon']} {comp['title']}</h3>
                <p style="line-height: 1.6;">{comp['description']}</p>
            </div>
        """, unsafe_allow_html=True)

# Chunking strategies comparison
st.markdown("## 🔀 Chunking Strategies Comparison")

st.markdown("""
    <table class="comparison-table">
        <thead>
            <tr>
                <th>Strategy</th>
                <th>Best For</th>
                <th>Advantages</th>
                <th>Considerations</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>🔢 Fixed-Size</strong></td>
                <td>General documents</td>
                <td>Predictable size, configurable overlap</td>
                <td>May split sentences awkwardly</td>
            </tr>
            <tr>
                <td><strong>📝 Regex Sentence</strong></td>
                <td>Simple text</td>
                <td>Fast, preserves sentence boundaries</td>
                <td>Basic pattern matching</td>
            </tr>
            <tr>
                <td><strong>🎯 NLTK Sentence</strong></td>
                <td>Complex text</td>
                <td>Accurate sentence detection</td>
                <td>Requires NLTK installation</td>
            </tr>
            <tr>
                <td><strong>📃 Paragraph</strong></td>
                <td>Structured documents</td>
                <td>Preserves natural structure</td>
                <td>Variable chunk sizes</td>
            </tr>
            <tr>
                <td><strong>🔄 Sliding Window</strong></td>
                <td>Dense information</td>
                <td>Ensures context continuity</td>
                <td>Higher redundancy</td>
            </tr>
            <tr>
                <td><strong>🌳 Recursive</strong></td>
                <td>Complex documents</td>
                <td>Intelligent splitting, preserves semantics</td>
                <td>More processing time</td>
            </tr>
        </tbody>
    </table>
""", unsafe_allow_html=True)

# Sliding window deep dive
st.markdown("## 🔄 Advanced Chunking Strategies")

tab1, tab2 = st.tabs(["🔄 Sliding Window", "🌳 Recursive Chunking"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <h3>How It Works</h3>
                <p style="line-height: 1.8;">
                    The sliding window creates overlapping chunks by moving a fixed-size 
                    window across the text. The <strong>window size</strong> determines 
                    chunk length, while <strong>step size</strong> controls overlap.
                </p>
                <p style="line-height: 1.8;">
                    For example, with window=20 and step=10, each chunk contains 20 words 
                    and shares 10 words with the next chunk (50% overlap).
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <h3>Key Benefits</h3>
                <ul style="line-height: 1.8;">
                    <li><strong>Context Preservation:</strong> Information spanning boundaries isn't lost</li>
                    <li><strong>Improved Recall:</strong> Same content appears in multiple chunks</li>
                    <li><strong>Flexible Control:</strong> Tune overlap for your needs</li>
                    <li><strong>Better Matches:</strong> Questions about edge content find answers</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <h3>How It Works</h3>
                <p style="line-height: 1.8;">
                    Recursive chunking uses a <strong>hierarchy of separators</strong> to intelligently 
                    split text while preserving semantic meaning:
                </p>
                <ol style="line-height: 1.8;">
                    <li><strong>Paragraphs</strong> (\\n\\n) - First priority</li>
                    <li><strong>Lines</strong> (\\n) - If paragraphs too large</li>
                    <li><strong>Sentences</strong> (. ! ?) - For finer splits</li>
                    <li><strong>Clauses</strong> (; ,) - Even finer splits</li>
                    <li><strong>Words</strong> (spaces) - As needed</li>
                    <li><strong>Characters</strong> - Last resort</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <h3>Key Benefits</h3>
                <ul style="line-height: 1.8;">
                    <li><strong>Semantic Boundaries:</strong> Respects natural text structure</li>
                    <li><strong>Adaptive:</strong> Adjusts strategy based on content</li>
                    <li><strong>Context-Aware:</strong> Keeps related information together</li>
                    <li><strong>Optimal Size:</strong> Targets ideal chunk size while preserving meaning</li>
                    <li><strong>Overlap Support:</strong> Maintains context across chunks</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="feature-card">
            <h3>🎯 When to Use Recursive Chunking</h3>
            <p style="line-height: 1.8;">
                Recursive chunking excels with:
            </p>
            <ul style="line-height: 1.8;">
                <li><strong>Complex documents:</strong> Research papers, legal documents, technical manuals</li>
                <li><strong>Mixed content:</strong> Documents with varying structure (lists, paragraphs, sections)</li>
                <li><strong>Long-form text:</strong> Books, articles, reports where context matters</li>
                <li><strong>Semantic queries:</strong> When you need chunks that respect topic boundaries</li>
            </ul>
            <p style="line-height: 1.8; margin-top: 1rem;">
                <strong>Example:</strong> With a target chunk size of 500 characters, the algorithm first tries 
                to split at paragraph boundaries. If a paragraph exceeds 500 characters, it recursively splits 
                by sentences, and so on down the hierarchy until optimal chunks are created.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Application architecture
st.markdown("## 🏗️ Application Architecture")

st.markdown("""
    <div class="feature-card">
        <h3>Pages & Navigation</h3>
        <ul style="line-height: 1.8;">
            <li><strong>🏠 Main Page:</strong> Primary interface for uploading documents and asking questions</li>
            <li><strong>📄 View Document:</strong> Inspect the complete source text being analyzed</li>
            <li><strong>ℹ️ About (This Page):</strong> Learn about system design, features, and best practices</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Important notes
st.markdown("## ⚠️ Important Notes")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="feature-card">
            <h3>What This System IS</h3>
            <ul style="line-height: 1.8;">
                <li>✅ Educational demonstration</li>
                <li>✅ Classical NLP techniques</li>
                <li>✅ Accurate text retrieval</li>
                <li>✅ Transparent methodology</li>
                <li>✅ Fast and lightweight</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <h3>What This System IS NOT</h3>
            <ul style="line-height: 1.8;">
                <li>❌ Large Language Model (LLM)</li>
                <li>❌ Generative AI system</li>
                <li>❌ Production-ready solution</li>
                <li>❌ Capable of inference</li>
                <li>❌ Able to hallucinate</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Technology stack
st.markdown("## 🛠️ Built With")

st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <span class="tech-badge">🎨 Streamlit</span>
        <span class="tech-badge">🔬 scikit-learn</span>
        <span class="tech-badge">🔢 NumPy</span>
        <span class="tech-badge">🐍 Python 3.10+</span>
        <span class="tech-badge">📝 NLTK</span>
        <span class="tech-badge">🎯 TF-IDF</span>
        <span class="tech-badge">📐 Cosine Similarity</span>
    </div>
""", unsafe_allow_html=True)

# Best practices
st.markdown("## 💡 Best Practices")

practices = [
    {
        "title": "Choose the Right Strategy",
        "content": "Match your chunking strategy to your document type. Use paragraph chunking for well-structured documents, sliding window for dense information."
    },
    {
        "title": "Tune Parameters",
        "content": "Experiment with chunk sizes and overlap. Larger chunks provide more context but may dilute relevance. More overlap improves recall but increases processing."
    },
    {
        "title": "Ask Specific Questions",
        "content": "Frame questions clearly with relevant keywords. Instead of 'What happened?', ask 'What awards did Maryam Mirzakhani receive?'"
    },
    {
        "title": "Check Similarity Scores",
        "content": "Scores above 0.5 indicate strong relevance. Low scores suggest the answer may not be in the document or needs rephrasing."
    }
]

for practice in practices:
    st.markdown(f"""
        <div class="feature-card">
            <h4>📌 {practice['title']}</h4>
            <p style="line-height: 1.8;">{practice['content']}</p>
        </div>
    """, unsafe_allow_html=True)

# Call to action
st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 10px; text-align: center; margin-top: 2rem;">
        <h3 style="color: white; margin: 0;">Ready to Explore?</h3>
        <p style="color: rgba(255, 255, 255, 0.9); margin: 1rem 0;">
            Head back to the main page and start asking questions about your documents!
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("👈 Use the sidebar to navigate back to the main RAG interface")

# --- Developer Credit in Sidebar ---
render_developer_info()
