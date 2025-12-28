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

def chunk_semantic(text: str, buffer_size: int = 1, breakpoint_threshold: float = 0.5) -> List[str]:
    """
    Implements semantic chunking by comparing sentence embeddings.
    Splits text when semantic similarity between consecutive sentences drops below threshold.
    
    Args:
        text: Input text to chunk
        buffer_size: Number of sentences to combine for comparison
        breakpoint_threshold: Similarity threshold for creating chunk boundaries (0-1)
    
    Returns:
        List of semantically coherent text chunks
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    
    # Split into sentences using regex
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s for s in sentences if s.strip()]
    
    if len(sentences) <= 1:
        return sentences
    
    # Create sentence embeddings using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        sentence_vectors = vectorizer.fit_transform(sentences)
    except ValueError:
        # If vectorization fails (e.g., all stop words), return original sentences
        return sentences
    
    # Calculate similarities between consecutive sentence groups
    similarities = []
    for i in range(len(sentences) - buffer_size):
        # Compare groups of sentences
        group1_indices = range(i, min(i + buffer_size, len(sentences)))
        group2_indices = range(i + buffer_size, min(i + 2 * buffer_size, len(sentences)))
        
        if not group2_indices:
            break
        
        # Average vectors for each group
        group1_vec = sentence_vectors[list(group1_indices)].toarray().mean(axis=0, keepdims=True)
        group2_vec = sentence_vectors[list(group2_indices)].toarray().mean(axis=0, keepdims=True)

        
        # Calculate similarity
        sim = cosine_similarity(group1_vec, group2_vec)[0][0]
        similarities.append(sim)
    
    # Find breakpoints where similarity drops below threshold
    chunks = []
    current_chunk = [sentences[0]]
    
    for i, sim in enumerate(similarities):
        sentence_idx = i + buffer_size
        if sentence_idx < len(sentences):
            if sim < breakpoint_threshold:
                # Similarity dropped - create new chunk
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentences[sentence_idx]]
            else:
                # Continue building current chunk
                current_chunk.append(sentences[sentence_idx])
    
    # Add remaining sentences
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return [chunk.strip() for chunk in chunks if chunk.strip()]

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


def chunk_hierarchical(text: str, max_chunk_size: int = 1000, preserve_structure: bool = True) -> List[str]:
    """
    Implements content-aware / hierarchical chunking that respects document structure.
    Identifies and preserves headings, sections, lists, and other structural elements.
    
    Args:
        text: Input text to chunk
        max_chunk_size: Maximum chunk size in characters
        preserve_structure: Whether to keep structural elements with their content
    
    Returns:
        List of hierarchically organized text chunks
    """
    
    class StructuralElement:
        """Represents a structural element in the document"""
        def __init__(self, content: str, element_type: str, level: int = 0):
            self.content = content
            self.element_type = element_type  # 'heading', 'list', 'paragraph', 'section'
            self.level = level  # Hierarchy level (0=top, 1=subsection, etc.)
            self.children = []
        
        def __repr__(self):
            return f"{self.element_type}(level={self.level}, len={len(self.content)})"
    
    def detect_heading(line: str) -> tuple:
        """
        Detects if a line is a heading and returns (is_heading, level, content)
        Supports Markdown-style (#, ##, ###) and underlined headings
        """
        line = line.strip()
        
        # Markdown-style headings
        markdown_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if markdown_match:
            level = len(markdown_match.group(1))
            content = markdown_match.group(2)
            return True, level, content
        
        # Detect underlined headings (next line is ====== or ------)
        # This is handled in parse_structure function
        
        # Heuristic: Short lines (< 50 chars) ending without punctuation might be headings
        if len(line) < 50 and line and not line[-1] in '.!?,;:':
            # Check if line is in Title Case or ALL CAPS
            if line.isupper() or (line[0].isupper() and sum(1 for c in line if c.isupper()) > len(line) * 0.3):
                return True, 1, line
        
        return False, 0, line
    
    def detect_list_item(line: str) -> tuple:
        """Detects if a line is a list item and returns (is_list, content)"""
        line_stripped = line.strip()
        
        # Bullet points: -, *, •
        if re.match(r'^[-*•]\s+', line_stripped):
            return True, re.sub(r'^[-*•]\s+', '', line_stripped)
        
        # Numbered lists: 1. 2. etc.
        if re.match(r'^\d+[\.)]\s+', line_stripped):
            return True, re.sub(r'^\d+[\.)]\s+', '', line_stripped)
        
        # Lettered lists: a) b) etc.
        if re.match(r'^[a-z][\.)]\s+', line_stripped):
            return True, re.sub(r'^[a-z][\.)]\s+', '', line_stripped)
        
        return False, line_stripped
    
    def parse_structure(text: str) -> List[StructuralElement]:
        """Parse text into structural elements"""
        lines = text.split('\n')
        elements = []
        current_paragraph = []
        current_list = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Check for underlined heading (current line + next line of ====)
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if re.match(r'^=+$', next_line) and len(next_line) >= 3:
                    # This is a level 1 heading
                    if current_paragraph:
                        elements.append(StructuralElement(' '.join(current_paragraph), 'paragraph'))
                        current_paragraph = []
                    if current_list:
                        elements.append(StructuralElement('\n'.join(current_list), 'list'))
                        current_list = []
                    elements.append(StructuralElement(line.strip(), 'heading', 1))
                    i += 2
                    continue
                elif re.match(r'^-+$', next_line) and len(next_line) >= 3:
                    # This is a level 2 heading
                    if current_paragraph:
                        elements.append(StructuralElement(' '.join(current_paragraph), 'paragraph'))
                        current_paragraph = []
                    if current_list:
                        elements.append(StructuralElement('\n'.join(current_list), 'list'))
                        current_list = []
                    elements.append(StructuralElement(line.strip(), 'heading', 2))
                    i += 2
                    continue
            
            # Empty line - end current paragraph/list
            if not line.strip():
                if current_paragraph:
                    elements.append(StructuralElement(' '.join(current_paragraph), 'paragraph'))
                    current_paragraph = []
                if current_list:
                    elements.append(StructuralElement('\n'.join(current_list), 'list'))
                    current_list = []
                i += 1
                continue
            
            # Check for heading
            is_heading, level, content = detect_heading(line)
            if is_heading:
                if current_paragraph:
                    elements.append(StructuralElement(' '.join(current_paragraph), 'paragraph'))
                    current_paragraph = []
                if current_list:
                    elements.append(StructuralElement('\n'.join(current_list), 'list'))
                    current_list = []
                elements.append(StructuralElement(content, 'heading', level))
                i += 1
                continue
            
            # Check for list item
            is_list, content = detect_list_item(line)
            if is_list:
                if current_paragraph:
                    elements.append(StructuralElement(' '.join(current_paragraph), 'paragraph'))
                    current_paragraph = []
                current_list.append(content)
                i += 1
                continue
            
            # Regular paragraph line
            if current_list:
                elements.append(StructuralElement('\n'.join(current_list), 'list'))
                current_list = []
            current_paragraph.append(line.strip())
            i += 1
        
        # Add remaining content
        if current_paragraph:
            elements.append(StructuralElement(' '.join(current_paragraph), 'paragraph'))
        if current_list:
            elements.append(StructuralElement('\n'.join(current_list), 'list'))
        
        return elements
    
    def create_chunks_from_elements(elements: List[StructuralElement]) -> List[str]:
        """Create chunks from structural elements while respecting hierarchy"""
        chunks = []
        current_chunk = []
        current_size = 0
        current_heading = None
        
        for element in elements:
            element_size = len(element.content)
            
            # If element is a heading
            if element.element_type == 'heading':
                # Save current chunk if it exists
                if current_chunk:
                    chunks.append('\n\n'.join(current_chunk))
                    current_chunk = []
                    current_size = 0
                
                # Start new chunk with heading
                current_heading = element.content
                if preserve_structure:
                    current_chunk.append(f"{'#' * element.level} {element.content}")
                    current_size = len(current_chunk[0])
                else:
                    current_chunk.append(element.content)
                    current_size = element_size
            
            # If adding this element would exceed max_chunk_size
            elif current_size + element_size + 2 > max_chunk_size:  # +2 for \n\n
                # Save current chunk
                if current_chunk:
                    chunks.append('\n\n'.join(current_chunk))
                
                # Start new chunk
                if preserve_structure and current_heading:
                    # Include heading context in new chunk
                    current_chunk = [f"[Continued from: {current_heading}]", element.content]
                    current_size = len(current_chunk[0]) + element_size + 2
                else:
                    current_chunk = [element.content]
                    current_size = element_size
            
            else:
                # Add element to current chunk
                current_chunk.append(element.content)
                current_size += element_size + 2  # +2 for \n\n
        
        # Add final chunk
        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))
        
        return chunks
    
    # Parse document structure
    elements = parse_structure(text)
    
    # Create chunks respecting structure
    chunks = create_chunks_from_elements(elements)
    
    return [chunk.strip() for chunk in chunks if chunk.strip()]


# ===== RAG SYSTEM =====

class SimpleRAG:
    def __init__(self, chunking_method: str = "fixed", chunk_size: int = 15, overlap: int = 0, 
                 window_size: int = 20, step_size: int = 10, 
                 recursive_chunk_size: int = 500, recursive_overlap: int = 50,
                 semantic_buffer_size: int = 1, semantic_threshold: float = 0.5,
                 hierarchical_max_size: int = 1000, hierarchical_preserve: bool = True,
                 _nltk_available: bool = True):
        self.chunking_method = chunking_method
        self.chunk_size = chunk_size
        self.overlap = overlap if chunking_method == "fixed" else 0
        self.window_size = window_size
        self.step_size = step_size
        self.recursive_chunk_size = recursive_chunk_size
        self.recursive_overlap = recursive_overlap
        self.semantic_buffer_size = semantic_buffer_size
        self.semantic_threshold = semantic_threshold
        self.hierarchical_max_size = hierarchical_max_size
        self.hierarchical_preserve = hierarchical_preserve
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
        elif self.chunking_method == "semantic":
            return chunk_semantic(text, self.semantic_buffer_size, self.semantic_threshold)
        elif self.chunking_method == "hierarchical":
            return chunk_hierarchical(text, self.hierarchical_max_size, self.hierarchical_preserve)
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
    