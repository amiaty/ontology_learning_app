import streamlit as st
import os
import sys

# Add parent directory to path to import methods
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import load_text_file

st.set_page_config(page_title="Evaluation", page_icon="📊")
st.title("Ontology Evaluation")

with st.expander("About this page", expanded=False):
    st.markdown("""
    This page allows you to evaluate your generated ontology against a reference.
    Upload both ontologies in TTL format to calculate quality metrics.
    """)

# Reference ontology
st.subheader("Reference Ontology")
ref_file = st.file_uploader("Upload reference ontology (TTL)", type="ttl")
if ref_file is not None:
    ref_content = ref_file.getvalue().decode("utf-8")
    st.text_area("Reference content", ref_content, height=150)
else:
    ref_content = ""

# Generated ontology
st.subheader("Generated Ontology")
gen_file = st.file_uploader("Upload generated ontology (TTL)", type="ttl")
if gen_file is not None:
    gen_content = gen_file.getvalue().decode("utf-8")
    st.text_area("Generated content", gen_content, height=150)
else:
    gen_content = ""

# Calculate metrics
if st.button("Calculate Metrics") and gen_content and ref_content:
    with st.spinner("Calculating metrics..."):
        # Placeholder for calculation
        completeness = 0.75
        conciseness = 0.82
        correctness = 0.78
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Completeness", f"{completeness:.2f}")
        col2.metric("Conciseness", f"{conciseness:.2f}")
        col3.metric("Correctness", f"{correctness:.2f}")
        
        # Placeholder for detailed comparison
        st.subheader("Detailed Comparison")
        st.write("This would show a detailed comparison between the ontologies")