import streamlit as st


def rag_question_answering():
    st.set_page_config(page_title="Advanced RAG Demo", layout="centered")
    st.title("RAG Question Answering")
    st.markdown("Upload a `.txt` file and ask questions about its content.")

def render_developer_info():
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Developed by:")
    st.sidebar.markdown("**Mohsen Moghimbegloo**")
    st.sidebar.markdown("[LinkedIn](https://linkedin.com/in/mohsen-moghimbegloo)")
    st.sidebar.markdown("[X (Twitter)](https://x.com/Moghimbegloo)")
    st.sidebar.markdown("[YouTube](https://www.youtube.com/@mohsenmoghimbegloo)")