import streamlit as st
import numpy as np
import pickle

# Page config
st.set_page_config(
    page_title="Sperm DF% Prediction Tool",
    page_icon="🧬",
    layout="wide"
)

# Custom CSS for smaller input boxes and transparent purple background
st.markdown("""
<style>
input {
    height: 30px !important;
    background-color: rgba(128, 0, 128, 0.1) !important; /* Transparent purple */
    border-radius: 8px !important;
    font-size: 16px !important;
}
</style>
""", unsafe_allow_html=True)

# Load the trained model
@st.cache_resource
def load_model():
    with open('ensemble_model.pkl', 'rb') as model_file:
        return pickle.load(model_file)

try:
    model = load_model()
    
    # App title and description
    st.title('🧬 Sperm DNA Fragmentation Percentage Prediction Tool 💦')
    st.write("""
    Predict the **DNA Fragmentation Percentage (DF%)** of sperm based on key **seminal fluid parameters**.
    The model uses a combination of various techniques to provide an accurate estimate of sperm DNA fragmentation.
    """)

    # Disclaimer
    st.markdown('---')
    st.markdown("""
    **Disclaimer**: This DF% prediction tool is not a diagnostic tool. It is based on a model built using **limited training data** 
    and the **chromatin dispersion assay**. The results should be interpreted with caution and are not a substitute for medical advice 
    or clinical diagnostics. Please consult a healthcare professional for proper evaluation.
    """)

except Exception as e:
    st.error(f'An error occurred: {str(e)}')
    st.info('Please make sure all model files are properly loaded and try again.')
