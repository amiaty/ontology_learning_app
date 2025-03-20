import streamlit as st

st.set_page_config(page_title="Settings", page_icon="⚙️")
st.title("Settings")

# API Configuration
st.subheader("API Configuration")
api_key = st.text_input("OpenAI API Key", type="password")
if st.button("Save API Key"):
    # Placeholder for saving API key
    st.success("API key saved!")

# Output Settings
st.subheader("Output Settings")
output_format = st.selectbox("Default Output Format", ["TTL", "RDF/XML", "JSON-LD"])

# Save all settings
if st.button("Save All Settings"):
    # Placeholder for saving settings
    st.success("Settings saved successfully!")