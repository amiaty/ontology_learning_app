
import streamlit as st
import os
import sys
import json
import pandas as pd

# Add parent directory to path to import methods
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from methods.metrics import calculate_metrics
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
        try:
            # Save temporary files for the metrics calculation
            with open("temp_ref.ttl", "w") as f:
                f.write(ref_content)
            with open("temp_gen.ttl", "w") as f:
                f.write(gen_content)
                
            # Calculate metrics using the refined method
            metrics = calculate_metrics("temp_ref.ttl", "temp_gen.ttl")
            
            # Clean up temporary files
            if os.path.exists("temp_ref.ttl"):
                os.remove("temp_ref.ttl")
            if os.path.exists("temp_gen.ttl"):
                os.remove("temp_gen.ttl")
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Completeness", f"{metrics['completeness']:.2f}")
            col2.metric("Conciseness", f"{metrics['conciseness']:.2f}")
            col3.metric("Correctness", f"{metrics['correctness']:.2f}")
            
            # Display detailed metrics
            st.subheader("Detailed Metrics")
            
            metrics_df = pd.DataFrame({
                'Metric': ['Classes', 'Data Properties', 'Object Properties', 
                           'Individuals', 'Axioms', 'Logical Axioms'],
                'Reference': [metrics['ref_classes'], metrics['ref_data_props'], 
                              metrics['ref_obj_props'], metrics['ref_individuals'], 
                              metrics['ref_axioms'], metrics['ref_logical_axioms']],
                'Generated': [metrics['gen_classes'], metrics['gen_data_props'], 
                              metrics['gen_obj_props'], metrics['gen_individuals'], 
                              metrics['gen_axioms'], metrics['gen_logical_axioms']],
                'Common': [metrics['common_classes'], metrics['common_data_props'], 
                           metrics['common_obj_props'], metrics['common_individuals'], 
                           metrics['common_axioms'], metrics['common_logical_axioms']]
            })
            
            st.table(metrics_df)
            
            # Display graph of metrics
            metrics_chart_data = pd.DataFrame({
                'Category': ['Classes', 'Properties', 'Individuals', 'Axioms'],
                'Completeness': [
                    metrics['common_classes']/metrics['ref_classes'] if metrics['ref_classes'] > 0 else 0,
                    (metrics['common_data_props'] + metrics['common_obj_props'])/(metrics['ref_data_props'] + metrics['ref_obj_props']) if (metrics['ref_data_props'] + metrics['ref_obj_props']) > 0 else 0,
                    metrics['common_individuals']/metrics['ref_individuals'] if metrics['ref_individuals'] > 0 else 0,
                    metrics['common_axioms']/metrics['ref_axioms'] if metrics['ref_axioms'] > 0 else 0
                ],
                'Conciseness': [
                    metrics['common_classes']/metrics['gen_classes'] if metrics['gen_classes'] > 0 else 0,
                    (metrics['common_data_props'] + metrics['common_obj_props'])/(metrics['gen_data_props'] + metrics['gen_obj_props']) if (metrics['gen_data_props'] + metrics['gen_obj_props']) > 0 else 0,
                    metrics['common_individuals']/metrics['gen_individuals'] if metrics['gen_individuals'] > 0 else 0,
                    metrics['common_axioms']/metrics['gen_axioms'] if metrics['gen_axioms'] > 0 else 0
                ]
            })
            
            st.bar_chart(metrics_chart_data.melt('Category', var_name='Metric', value_name='Score'))
            
        except Exception as e:
            st.error(f"Error calculating metrics: {str(e)}")