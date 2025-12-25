import streamlit as st


def ensure_nltk_punkt() -> bool:
    """
    Checks if NLTK 'punkt' tokenizer is available.
    If not, attempts to download it with a Streamlit spinner.
    Returns True if available (after download or already present), False otherwise.
    """
    try:
        import nltk
        # Check if 'punkt' is already available
        if nltk.data.find('tokenizers/punkt'):
            return True
        else:
            with st.spinner("Downloading NLTK 'punkt' tokenizer (one-time)..."):
                nltk.download('punkt', quiet=True)
            return True
    except Exception:
        return False
    