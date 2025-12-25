import streamlit as st
from ui_components import render_developer_info


st.set_page_config(page_title="About This App", layout="centered")

st.title("About This Application")

st.markdown("""
This application presents a lightweight, educational implementation of a **Retrieval-Augmented Generation (RAG)** system. It enables question-answering over a static document—currently a biographical text about **Maryam Mirzakhani**, the first woman to win the Fields Medal—using classical natural language processing techniques.
""")

st.markdown("### Core Components")
st.markdown("""
- **Text Chunking**: Splits the source document using configurable strategies (fixed-size, sentence-based with regex or NLTK, paragraph-based, or sliding window).
- **TF-IDF Vectorization**: Transforms text chunks and queries into numerical vectors.
- **Cosine Similarity**: Measures semantic relevance between a query and document chunks.
- **Response Synthesis**: Combines top-retrieved chunks into a coherent answer.
""")

st.markdown("### Chunking Strategies")
st.markdown("""
- **Fixed-Size**: Splits text into chunks of a specified word count with optional overlap.
- **Regex (Sentence)**: Uses regular expressions to split text at sentence boundaries.
- **NLTK (Sentence)**: Uses NLTK's advanced sentence tokenizer for more accurate sentence detection.
- **Paragraph**: Splits text at paragraph breaks (double newlines), preserving natural document structure.
- **Sliding Window**: Implements overlapping chunks where each chunk shares content with adjacent chunks. The window size determines chunk length, while step size controls how much the window moves forward (smaller step = more overlap).
""")

st.markdown("### Sliding Window Advantages")
st.markdown("""
The sliding window approach offers several benefits:
- **Contextual Continuity**: Overlapping content ensures important information spanning chunk boundaries isn't lost.
- **Improved Retrieval**: Multiple chunks may contain the same key information, increasing retrieval accuracy.
- **Flexible Control**: Adjust window and step sizes to balance between redundancy and coverage.
- **Better for Questions**: Queries about concepts mentioned near chunk boundaries are more likely to find relevant matches.
""")

st.markdown("### Application Structure")
st.markdown("""
- **Main Page**: Interact with the RAG system by asking questions.
- **View Document**: Inspect the full source text used by the retriever.
- **This Page**: Learn about the system's design, limitations, and technologies.
""")

st.markdown("### Important Notes")
st.markdown("""
- This is **not a large language model (LLM)** and does **not generate novel answers**.  
- Responses are **directly constructed from retrieved text fragments**—no hallucination, but also no inference.
- Designed for **learning and demonstration purposes**, not production use.
""")

st.markdown("### Built With")
st.markdown("""
- **Streamlit** – for the interactive web interface  
- **scikit-learn** – for TF-IDF and cosine similarity  
- **NumPy** – for numerical operations  
- **Standard Python libraries** – `re`, `os`, and optional `nltk`
""")

st.markdown("👈 Navigate using the sidebar to return to the main interface or explore the full document.")

# --- Developer Credit in Sidebar ---
render_developer_info()
