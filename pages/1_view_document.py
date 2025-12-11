import streamlit as st
import os

st.set_page_config(page_title="View Document", layout="wide")
st.title("📄 Full Document Content")

DOC_PATH = "./content.txt"

if os.path.exists(DOC_PATH):
    with open(DOC_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    st.text_area("Document:", content, height=600)
else:
    st.error("Document file not found!")

st.markdown("👈 Use the sidebar to return to the **main RAG page**.")

# --- Developer Credit in Sidebar (appears on all pages) ---
st.sidebar.markdown("### Developed by:")
st.sidebar.markdown("**Mohsen Moghimbegloo**")
st.sidebar.markdown("[LinkedIn](https://linkedin.com/in/mohsen-moghimbegloo)")
st.sidebar.markdown("[X (Twitter)](https://x.com/Moghimbegloo)")
st.sidebar.markdown("[YouTube](https://www.youtube.com/@mohsenmoghimbegloo)")
