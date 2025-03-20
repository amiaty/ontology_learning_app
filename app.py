import streamlit as st

st.set_page_config(
    page_title="Ontology Learning from Text",
    page_icon="🧠",
    layout="wide"
)


st.title("Ontology Learning from Text Using NLP")

st.markdown("""
This application helps you generate ontologies from unstructured text using NLP techniques.

**Getting Started:**
1. Configure your API keys in the Settings page
2. Navigate to the Learning page to create ontologies
3. Use the Evaluation page to compare with ground truth
""")

st.sidebar.success("Select a page from the sidebar")