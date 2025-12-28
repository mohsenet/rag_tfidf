import streamlit as st
from io import StringIO


def init_session_state():
    """
    Initialize default values in st.session_state if not already set.
    This function should be called at the start of the application to ensure
    all required session state variables exist with appropriate default values.
    """
    
    # Document-related state
    if "document_text" not in st.session_state:
        st.session_state.document_text = None
    
    if "document_name" not in st.session_state:
        st.session_state.document_name = None

    # Chunking strategy selection
    if "chunking_choice" not in st.session_state:
        st.session_state.chunking_choice = "fixed"

    # Fixed-size chunking parameters
    if "chunk_size" not in st.session_state:
        st.session_state.chunk_size = 10

    if "overlap" not in st.session_state:
        st.session_state.overlap = 2
    
    # Sliding window chunking parameters
    if "window_size" not in st.session_state:
        st.session_state.window_size = 20
    
    if "step_size" not in st.session_state:
        st.session_state.step_size = 10
    
    # Recursive chunking parameters
    if "recursive_chunk_size" not in st.session_state:
        st.session_state.recursive_chunk_size = 500
    
    if "recursive_overlap" not in st.session_state:
        st.session_state.recursive_overlap = 50
    
    # Semantic chunking parameters
    if "semantic_buffer_size" not in st.session_state:
        st.session_state.semantic_buffer_size = 1
    
    if "semantic_threshold" not in st.session_state:
        st.session_state.semantic_threshold = 0.5
    
    # Hierarchical chunking parameters
    if "hierarchical_max_size" not in st.session_state:
        st.session_state.hierarchical_max_size = 1000
    
    if "hierarchical_preserve" not in st.session_state:
        st.session_state.hierarchical_preserve = True


def handle_uploaded_file(uploaded_file):
    """
    Process an uploaded file and update session state with its contents.
    
    Args:
        uploaded_file: Streamlit UploadedFile object from st.file_uploader
    
    Updates session state with:
        - document_text: The full text content of the uploaded file
        - document_name: The name of the uploaded file
    
    Displays a success message when file is successfully uploaded.
    """
    if uploaded_file is not None:
        try:
            # Read the uploaded file content
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            document_content = stringio.read()
            
            # Update session state
            st.session_state.document_text = document_content
            st.session_state.document_name = uploaded_file.name
            
            # Show success message
            st.success(f"✅ Uploaded: `{uploaded_file.name}`")
            
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.session_state.document_text = None
            st.session_state.document_name = None
            