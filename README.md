# 🔍 Advanced RAG Question Answering System

A comprehensive Retrieval-Augmented Generation (RAG) system using classical NLP techniques. Features 8 chunking strategies, TF-IDF vectorization, and an interactive Streamlit UI.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- **8 Chunking Strategies**: Fixed-size, Sentence (Regex/NLTK), Paragraph, Sliding Window, Recursive, Semantic, Hierarchical
- **TF-IDF Vectorization**: Convert text into meaningful numerical representations
- **Cosine Similarity Search**: Find most relevant document chunks
- **Interactive UI**: Beautiful Streamlit interface with real-time configuration
- **Document Viewer**: Inspect source documents with statistics

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/rag_tfidf.git
cd rag_tfidf

# Using uv
uv sync
source .venv/bin/activate

# Run Application
streamlit run src/rag_app.py
```



Open browser at `http://localhost:8501`

## 📖 Usage

1. **Upload Document** - Select a `.txt` file or use the sample document
2. **Choose Strategy** - Pick from 8 chunking strategies in the sidebar
3. **Adjust Parameters** - Fine-tune chunk size, overlap, thresholds
4. **Ask Questions** - Type your query and get AI-powered answers

## 🎯 Chunking Strategy Guide

| Strategy | Best For | When to Use |
|----------|----------|-------------|
| **Fixed-Size** | General documents | Consistent chunk sizes needed |
| **Sentence (Regex/NLTK)** | Simple/complex text | Preserve sentence boundaries |
| **Paragraph** | Structured documents | Natural paragraph breaks exist |
| **Sliding Window** | Dense information | Context continuity critical |
| **Recursive** | Mixed content | Variable structure documents |
| **Semantic** | Topic-based content | Natural topic boundaries wanted |
| **Hierarchical** | Structured docs | Headings/sections present |

### Recommended Parameters

- **Fixed**: 15-30 words, 10-20% overlap
- **Sliding Window**: 20-40 words window, 50-70% step size
- **Recursive**: 500-1000 chars, 50-100 char overlap
- **Semantic**: 2-3 sentence buffer, 0.5-0.6 threshold
- **Hierarchical**: 1000-2000 chars, preserve context enabled

## 📁 Project Structure

```
rag_tfidf/
├── src/
│   ├── rag_app.py              # Main application
│   ├── rag_engine.py            # Core RAG with chunking strategies
│   ├── rag_builder.py           # RAG instance builder
│   ├── session.py               # Session state management
│   ├── ui_components.py         # UI rendering
│   ├── query_handler.py         # Query processing
│   ├── utils.py                 # Utilities
│   ├── content.txt              # Sample document
│   └── pages/
│       ├── 1_view_document.py   # Document viewer
│       └── 2_about_app.py       # Documentation
├── main.py                      # App launcher
└── pyproject.toml               # Dependencies
```

## 🧪 Testing

```bash
# Test chunking strategies
python -c "
from src.rag_engine import SimpleRAG
rag = SimpleRAG(chunking_method='hierarchical')
rag.add_documents(open('src/content.txt').read())
print(rag.generate_response('Who won the Fields Medal?'))
"
```

## 📊 Performance

| Strategy | Speed | Memory | Accuracy | Use Case |
|----------|-------|--------|----------|----------|
| Fixed-Size | ⚡⚡⚡ | Low | ⭐⭐ | Speed priority |
| Sentence | ⚡⚡⚡ | Low | ⭐⭐⭐ | Balanced |
| Sliding Window | ⚡⚡ | Medium | ⭐⭐⭐⭐ | Context important |
| Recursive | ⚡ | Low | ⭐⭐⭐⭐ | Complex docs |
| Semantic | ⚡ | Medium | ⭐⭐⭐⭐⭐ | Best accuracy |
| Hierarchical | ⚡⚡ | Low | ⭐⭐⭐⭐⭐ | Structured docs |

## 🎓 Learning Objectives

- Text chunking strategies
- TF-IDF vectorization
- Similarity search algorithms
- Building RAG systems
- Streamlit application development



## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 👨‍💻 Author

**Mohsen Moghimbegloo**

- [LinkedIn](https://linkedin.com/in/mohsen-moghimbegloo)
- [Twitter](https://x.com/Moghimbegloo)
- [YouTube](https://www.youtube.com/@mohsenmoghimbegloo)

---

⭐ **Star this repo if helpful!**