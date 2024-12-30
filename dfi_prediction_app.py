import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

# Page config
st.set_page_config(
    page_title="DFI Prediction Tool",
    page_icon="🧬",
    layout="wide"
)

# Load the trained model
@st.cache_resource
def load_model():
    with open('ensemble_model.pkl', 'rb') as model_file:
        return pickle.load(model_file)

try:
    model = load_model()
    
    # App title and description
    st.title('🧬 DFI Prediction Tool')
    st.write('Enter sperm parameters to predict DNA Fragmentation Index (DFI)')
    
    # Create two columns for inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('Motility Parameters')
        progressive = st.number_input('Progressive (%)', 0.0, 100.0, 50.0, 0.1)
        non_progressive = st.number_input('Non-progressive (%)', 0.0, 100.0, 10.0, 0.1)
        immotile = st.number_input('Immotile (%)', 0.0, 100.0, 40.0, 0.1)
    
    with col2:
        st.subheader('Other Parameters')
        concentration = st.number_input('Concentration (million/mL)', 0.0, 300.0, 50.0, 0.1)
        normal_sperm = st.number_input('Normal Morphology (%)', 0.0, 100.0, 14.0, 0.1)
        volume = st.number_input('Volume (mL)', 0.0, 10.0, 2.0, 0.1)  # New parameter
    
    # Add a predict button
    if st.button('Predict DFI', type='primary'):
        # Create input array
        input_features = np.array([[progressive, immotile, non_progressive, concentration, normal_sperm, volume]])
        
        # Make prediction
        prediction = model.predict(input_features)[0]
        
        # Display results
        st.markdown('---')
        st.subheader('Prediction Results')
        
        # Create columns for displaying results
        res_col1, res_col2, res_col3 = st.columns(3)
        
        with res_col2:
            st.metric(label="Predicted DFI", value=f"{prediction:.1f}%")
        
        # Add interpretation
        st.markdown('---')
        st.subheader('Interpretation Guide')
        if prediction < 15:
            st.success('DFI < 15%: Generally considered normal/good fertility potential')
        elif prediction < 25:
            st.warning('DFI 15-25%: Moderate fertility impact, may affect pregnancy outcomes')
        else:
            st.error('DFI > 25%: Higher impact on fertility, may indicate need for additional evaluation')

    # Add Disclaimer at the bottom or in the sidebar
    st.markdown('---')
    st.markdown("""
    **Disclaimer**: This DFI% prediction tool is not a diagnostic tool. It is based on a model built using **limited training data** 
    and the **chromatin dispersion assay**. The results should be interpreted with caution and are not a substitute for medical advice 
    or clinical diagnostics. Please consult a healthcare professional for proper evaluation.
    """)

except Exception as e:
    st.error(f'An error occurred: {str(e)}')
    st.info('Please make sure all model files are properly loaded and try again.')
