from typing import List, Tuple
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


# ===== CHUNKING STRATEGIES =====

def chunk_fixed_size_with_overlap(text: str, size: int = 15, overlap: int = 0) -> List[str]:
    if size <= 0:
        raise ValueError("Chunk size must be > 0")
    if overlap < 0:
        overlap = 0
    if overlap >= size:
        overlap = size - 1
    words = text.split()
    chunks = []
    step = size - overlap
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + size])
        if chunk:
            chunks.append(chunk)
    return chunks

def chunk_sentence_regex(text: str) -> List[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s]

def chunk_sentence_nltk(text: str, _nltk_available: bool = True) -> List[str]:
    if not _nltk_available:
        return chunk_sentence_regex(text)
    try:
        import nltk
        return nltk.sent_tokenize(text)
    except ImportError:
        return chunk_sentence_regex(text)

def chunk_paragraph(text: str) -> List[str]:
    """
    Splits text into paragraphs based on double newlines or multiple consecutive newlines.
    Filters out empty paragraphs and strips whitespace.
    """
    paragraphs = re.split(r'\n\s*\n', text.strip())
    return [p.strip() for p in paragraphs if p.strip()]

def chunk_sliding_window(text: str, window_size: int = 20, step_size: int = 10) -> List[str]:
    """
    Implements sliding window chunking where each chunk overlaps with the previous one.
    
    Args:
        text: Input text to chunk
        window_size: Number of words in each chunk
        step_size: Number of words to move forward for the next chunk (creates overlap when < window_size)
    
    Returns:
        List of text chunks with controlled overlap
    """
    if window_size <= 0:
        raise ValueError("Window size must be > 0")
    if step_size <= 0:
        raise ValueError("Step size must be > 0")
    if step_size > window_size:
        raise ValueError("Step size should not exceed window size for proper overlap")
    
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), step_size):
        chunk = " ".join(words[i:i + window_size])
        if chunk:
            chunks.append(chunk)
        # Stop if we've reached the end
        if i + window_size >= len(words):
            break
    
    return chunks


# ===== RAG SYSTEM =====

class SimpleRAG:
    def __init__(self, chunking_method: str = "fixed", chunk_size: int = 15, overlap: int = 0, 
                 window_size: int = 20, step_size: int = 10, _nltk_available: bool = True):
        self.chunking_method = chunking_method
        self.chunk_size = chunk_size
        self.overlap = overlap if chunking_method == "fixed" else 0
        self.window_size = window_size
        self.step_size = step_size
        self._nltk_available = _nltk_available
        self.chunks = []
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.chunk_vectors = None

    def _chunk_text(self, text: str) -> List[str]:
        if self.chunking_method == "fixed":
            return chunk_fixed_size_with_overlap(text, self.chunk_size, self.overlap)
        elif self.chunking_method == "regex":
            return chunk_sentence_regex(text)
        elif self.chunking_method == "nltk":
            return chunk_sentence_nltk(text, self._nltk_available)
        elif self.chunking_method == "paragraph":
            return chunk_paragraph(text)
        elif self.chunking_method == "sliding":
            return chunk_sliding_window(text, self.window_size, self.step_size)
        else:
            raise ValueError(f"Unknown method: {self.chunking_method}")

    def add_documents(self, text: str):
        self.chunks = self._chunk_text(text)
        if not self.chunks:
            raise ValueError("No chunks extracted.")
        self.chunk_vectors = self.vectorizer.fit_transform(self.chunks)

    def search_with_scores(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        if self.chunk_vectors is None or self.chunk_vectors.shape[0] == 0:
            return []
        query_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self.chunk_vectors).flatten()
        top_indices = sims.argsort()[-top_k:][::-1]
        return [(self.chunks[i], float(sims[i])) for i in top_indices]

    def generate_response(self, query: str, top_k=3):
        results = self.search_with_scores(query, top_k)
        if not results:
            return "I don't have enough information to answer that question."
        return f"Based on the information: {' '.join(chunk for chunk, _ in results)}"
