import streamlit as st
import os
import sys

# Add parent directory to path to import methods
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import load_text_file

st.set_page_config(page_title="Learning", page_icon="📚")
st.title("Ontology Learning")

with st.expander("About this page", expanded=False):
    st.markdown("""
    This page allows you to generate ontologies from text using OpenAI's language models.
    Upload your text file or enter text directly.
    """)

# Input section
st.subheader("Input Text")

input_option = st.radio("Select input method:", ["Upload file", "Enter text"])

if input_option == "Upload file":
    uploaded_file = st.file_uploader("Choose a text file", type="txt")
    if uploaded_file is not None:
        text_content = uploaded_file.getvalue().decode("utf-8")
        st.text_area("Text content", text_content, height=200)
else:
    text_content = st.text_area("Enter text", "", height=200)

# Parameters
st.subheader("Parameters")
model = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"])
temp = st.slider("Temperature", 0.0, 1.0, 1.0)

# Process button
if st.button("Generate Ontology"):
    with st.spinner("Generating ontology..."):
        st.info("This would call your ontology generation method")
        # Placeholder for actual implementation
        st.session_state.output_ontology = """
# Example TTL Output
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex: <http://example.org/ontology#> .

ex:Concept1 a rdfs:Class ;
    rdfs:label "Example Concept" ;
    rdfs:comment "This is an example concept generated from text." .
        """
        st.success("Ontology generated successfully!")

# Output display
if "output_ontology" in st.session_state:
    st.subheader("Generated Ontology")
    st.text_area("TTL Output", st.session_state.output_ontology, height=300)
    
    # Download button
    st.download_button(
        label="Download Ontology (TTL)",
        data=st.session_state.output_ontology,
        file_name="generated_ontology.ttl",
        mime="text/turtle"
    )