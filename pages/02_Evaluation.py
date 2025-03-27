# fancy_metrics_app.py
import streamlit as st
from methods.metrics import load_and_normalize, conciseness, completeness, correctness

# Application UI
st.set_page_config(page_title="Ontology Metrics Evaluation", layout="centered", initial_sidebar_state="expanded")

st.title("📊 **Ontology Metrics Evaluation Tool**")
st.write(
    "Evaluate your learned ontology against the ground truth using metrics such as **Conciseness**, "
    "**Completeness**, and **Correctness**. Upload your ontologies below to get started!"
)

# File Upload Section
st.sidebar.header("Upload Ontologies")
uploaded_learned_file = st.sidebar.file_uploader("Upload Learned Ontology (Turtle Format)", type="ttl")
uploaded_gt_file = st.sidebar.file_uploader("Upload Ground Truth Ontology (Turtle Format)", type="ttl")

if uploaded_learned_file and uploaded_gt_file:
    st.sidebar.success("✅ Both files uploaded successfully!")
    with st.spinner("🎛️ Processing ontologies and calculating metrics..."):
        # Load and normalize ontologies
        learned_triples = load_and_normalize(uploaded_learned_file)
        gt_triples = load_and_normalize(uploaded_gt_file)

        # Compute metrics
        conc = conciseness(learned_triples, gt_triples)
        comp = completeness(learned_triples, gt_triples)
        corr = correctness(learned_triples, gt_triples)

    # Results Section
    st.success("✨ Ontology metrics calculated successfully!")
    st.write("Below is an overview of your ontology's performance based on the calculated metrics:")

    # Fancy Output Section
    col1, col2, col3 = st.columns(3)

    # 1. Conciseness
    with col1:
        st.metric("🧩 Conciseness", f"{conc:.3f}", delta=None, help="The proportion of shared elements in the learned ontology compared to its total elements.")
        st.progress(conc)

    # 2. Completeness
    with col2:
        st.metric("📖 Completeness", f"{comp:.3f}", delta=None, help="The proportion of shared elements compared to the total reference ontology.")
        st.progress(comp)

    # 3. Correctness
    with col3:
        st.metric("✔️ Correctness", f"{corr:.3f}", delta=None, help="The harmonic mean of conciseness and completeness.")
        st.progress(corr)

    # Additional Explanation Section
    st.subheader("📃 Detailed Insights:")
    st.markdown(
        """
        - **Conciseness**: Measures how efficiently the learned ontology captures relevant elements.
        - **Completeness**: Indicates how well the learned ontology aligns with the domain's full scope.
        - **Correctness**: A harmonic balance between **Conciseness** and **Completeness**, providing an overall quality snapshot.
        """
    )

    st.info(
        f"**Pro Tip:** Higher scores (closer to 1.0) indicate better performance. Analyze the individual metrics carefully to pinpoint "
        f"areas for improvement in your ontology learning pipeline!"
    )

    # Debugging Insights (Optional, expandable)
    with st.expander("🔍 Debugging Information"):
        st.write("**Normalized Learned Triples:**", learned_triples)
        st.write("**Normalized Ground Truth Triples:**", gt_triples)
else:
    st.info("Please upload **both** the learned ontology and ground truth ontology to begin.")

