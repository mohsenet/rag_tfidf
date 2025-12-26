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

def chunk_recursive(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """
    Implements recursive chunking using a hierarchy of separators.
    Tries to split by paragraphs first, then sentences, then words.
    
    Args:
        text: Input text to chunk
        chunk_size: Target chunk size in characters
        chunk_overlap: Number of characters to overlap between chunks
    
    Returns:
        List of text chunks
    """
    if chunk_size <= 0:
        raise ValueError("Chunk size must be > 0")
    if chunk_overlap < 0:
        chunk_overlap = 0
    if chunk_overlap >= chunk_size:
        chunk_overlap = chunk_size - 1
    
    # Define separators in order of priority
    separators = [
        "\n\n",  # Paragraphs
        "\n",    # Lines
        ". ",    # Sentences
        "! ",    # Exclamations
        "? ",    # Questions
        "; ",    # Semicolons
        ", ",    # Commas
        " ",     # Words
        ""       # Characters (fallback)
    ]
    
    def split_text(text: str, separators: List[str]) -> List[str]:
        """Recursively split text using hierarchical separators."""
        if not separators:
            # Base case: no more separators, return character chunks
            return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size - chunk_overlap)]
        
        separator = separators[0]
        remaining_separators = separators[1:]
        
        if separator == "":
            # Last resort: split by characters
            return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size - chunk_overlap)]
        
        splits = text.split(separator)
        chunks = []
        current_chunk = ""
        
        for i, split in enumerate(splits):
            # Reconstruct with separator (except for last split)
            if i < len(splits) - 1:
                split = split + separator
            
            # If adding this split would exceed chunk_size, process current chunk
            if len(current_chunk) + len(split) > chunk_size and current_chunk:
                # If current chunk is still too large, recursively split it
                if len(current_chunk) > chunk_size:
                    sub_chunks = split_text(current_chunk, remaining_separators)
                    chunks.extend(sub_chunks)
                else:
                    chunks.append(current_chunk.strip())
                
                # Start new chunk with overlap
                if chunk_overlap > 0 and chunks:
                    # Take last chunk_overlap characters from previous chunk
                    overlap_text = current_chunk[-chunk_overlap:]
                    current_chunk = overlap_text + split
                else:
                    current_chunk = split
            else:
                current_chunk += split
        
        # Add remaining chunk
        if current_chunk.strip():
            if len(current_chunk) > chunk_size:
                sub_chunks = split_text(current_chunk, remaining_separators)
                chunks.extend(sub_chunks)
            else:
                chunks.append(current_chunk.strip())
        
        return chunks
    
    result = split_text(text, separators)
    # Filter out empty chunks
    return [chunk for chunk in result if chunk.strip()]


# ===== RAG SYSTEM =====

class SimpleRAG:
    def __init__(self, chunking_method: str = "fixed", chunk_size: int = 15, overlap: int = 0, 
                 window_size: int = 20, step_size: int = 10, 
                 recursive_chunk_size: int = 500, recursive_overlap: int = 50,
                 _nltk_available: bool = True):
        self.chunking_method = chunking_method
        self.chunk_size = chunk_size
        self.overlap = overlap if chunking_method == "fixed" else 0
        self.window_size = window_size
        self.step_size = step_size
        self.recursive_chunk_size = recursive_chunk_size
        self.recursive_overlap = recursive_overlap
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
        elif self.chunking_method == "recursive":
            return chunk_recursive(text, self.recursive_chunk_size, self.recursive_overlap)
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
    