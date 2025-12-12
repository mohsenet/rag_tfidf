import streamlit as st

st.set_page_config(page_title="View Document", layout="wide")
st.title("📄 Full Document Content")

# Try to get document from session state
document_text = st.session_state.get("document_text", None)
document_name = st.session_state.get("document_name", "Uploaded Document")

if document_text is not None:
    st.text_area(f"Content of '{document_name}':", document_text, height=600)
else:
    st.info(
        "No document uploaded yet. "
        "Please go to the **main RAG page**, upload a `.txt` file, and return here."
    )

st.markdown("👈 Use the sidebar to return to the **main RAG page** or upload a file.")

# --- Developer Credit in Sidebar ---
st.sidebar.markdown("---")
st.sidebar.markdown("### Developed by:")
st.sidebar.markdown("**Mohsen Moghimbegloo**")
st.sidebar.markdown("[LinkedIn](https://linkedin.com/in/mohsen-moghimbegloo)")
st.sidebar.markdown("[X (Twitter)](https://x.com/Moghimbegloo)")
st.sidebar.markdown("[YouTube](https://www.youtube.com/@mohsenmoghimbegloo)")