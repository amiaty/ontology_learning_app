import streamlit as st
import os
import sys
import json
import tempfile

from methods.text_to_ontology_prompt import generate_ontology_from_text, create_ontology_from_description
from utils import load_text_file, save_ontology

st.set_page_config(page_title="Learn Ontology", page_icon="🧠")
st.title("🧠 **Ontology Learning from Text**")

# Example of accessing settings in another page
api_key = st.session_state.api_key
output_format = st.session_state.output_format

# If no API key is set, prompt user
if not api_key:
    st.warning("Please configure your OpenAI API key in the Settings page first.")

# Input method selection
input_method = st.radio("Input Method", ["Upload File", "Enter Text"])

text_content = ""

if input_method == "Upload File":
    uploaded_file = st.file_uploader("Upload text file", type=["txt", "md", "json"])
    
    if uploaded_file is not None:
        text_content = uploaded_file.getvalue().decode("utf-8")
        st.text_area("File content", text_content, height=250)
else:
    text_content = st.text_area("Enter text for ontology learning", height=250)

# Model selection
model = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"])

# Output format
output_format = st.selectbox("Output Format", 
                           ["TTL", "RDF/XML", "JSON-LD"], 
                           index=["TTL", "RDF/XML", "JSON-LD"].index(output_format))

# Process
if st.button("Generate Ontology") and text_content:
    if not api_key:
        st.error("API key is required. Please configure it in the Settings page.")
    else:
        with st.spinner("Generating ontology..."):
            try:
                # Set OpenAI API key
                os.environ["OPENAI_API_KEY"] = api_key
                
                # Generate ontology
                # ontology_content = generate_ontology_from_text(text_content, model=model)
                ontology_content = create_ontology_from_description(text_content, model=model)
                # Display results
                st.subheader("Generated Ontology")
                st.text_area("Ontology (TTL)", ontology_content, height=400)
                
                # Download button
                st.download_button(
                    label="Download Ontology",
                    data=ontology_content,
                    file_name="generated_ontology.ttl",
                    mime="text/turtle"
                )
                
                
            except Exception as e:
                st.error(f"Error generating ontology: {str(e)}")