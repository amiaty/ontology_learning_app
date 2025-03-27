# pages/01_Settings.py
import streamlit as st

st.set_page_config(page_title="Settings", page_icon="⚙️")
st.title("⚙️ **Settings**")

# Initialize session state variables if they don't exist
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'output_format' not in st.session_state:
    st.session_state.output_format = "TTL"

# API Configuration
st.subheader("API Configuration")
api_key = st.text_input(
    "OpenAI API Key", 
    value=st.session_state.api_key,
    type="password",
    help="This key will be stored in session memory only and will reset when you close the browser"
)

# Output Settings
st.subheader("Output Settings")
output_format = st.selectbox(
    "Default Output Format", 
    ["TTL", "RDF/XML", "JSON-LD"], 
    index=["TTL", "RDF/XML", "JSON-LD"].index(st.session_state.output_format)
)

# Save to session state (not to disk)
if st.button("Apply Settings"):
    st.session_state.api_key = api_key
    st.session_state.output_format = output_format
    st.success("Settings applied for this session!")

# Information about session state
st.info("⚠️ These settings will reset when you refresh the app or close your browser. This is intended behavior for security reasons.")
