import streamlit as st
import numpy as np
import pickle

# Page config
st.set_page_config(
    page_title="DFI Prediction Tool",
    page_icon="🧬",
    layout="wide"
)

# Custom CSS for smaller input boxes and transparent purple color
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
    st.title('🧬 DFI Prediction Tool')
    st.write('Enter sperm parameters to predict DNA Fragmentation Index (DFI)')
    
    # Create a single column for inputs
    st.subheader('Input Parameters')

    # Input fields with emojis and smaller number boxes
    progressive = st.number_input('🚀 Progressive (%)', 0.0, 100.0, 50.0, 0.1)
    non_progressive = st.number_input('🐢 Non-progressive (%)', 0.0, 100.0, 10.0, 0.1)
    immotile = st.number_input('🛑 Immotile (%)', 0.0, 100.0, 40.0, 0.1)
    concentration = st.number_input('🔬 Concentration (million/mL)', 0.0, 300.0, 50.0, 0.1)
    normal_sperm = st.number_input('🌟 Normal Morphology (%)', 0.0, 100.0, 14.0, 0.1)

    # Add a predict button
    if st.button('Predict DFI', type='primary'):
        # Create input array
        input_features = np.array([[progressive, immotile, non_progressive, concentration, normal_sperm]])
        
        # Make prediction
        prediction = model.predict(input_features)[0]
        
        # Display results
        st.markdown('---')
        st.subheader('Prediction Results')
        
        # Determine result interpretation with emojis
        if prediction < 15:
            result = "🟢 Excellent fertility potential (DFI < 15%)"
            emoji = "😊"
        elif prediction < 25:
            result = "🟡 Moderate fertility impact (DFI 15-25%)"
            emoji = "😐"
        else:
            result = "🔴 High fertility impact (DFI > 25%)"
            emoji = "😟"
        
        # Display the result with DNA emoji
        st.metric(label="Predicted DFI", value=f"{prediction:.1f}% 🧬")
        st.write(f"Result: {result} {emoji}")
        
        # Add a colorful separator line
        st.markdown('---')
        st.subheader('Interpretation Guide')
        st.write("""
        - 🟢 **DFI < 15%**: Generally considered normal/good fertility potential.
        - 🟡 **DFI 15-25%**: Moderate fertility impact, may affect pregnancy outcomes.
        - 🔴 **DFI > 25%**: Higher impact on fertility, may indicate need for additional evaluation.
        """)
    
    # Add Disclaimer at the bottom
    st.markdown('---')
    st.markdown("""
    **Disclaimer**: This DFI% prediction tool is not a diagnostic tool. It is based on a model built using **limited training data** 
    and the **chromatin dispersion assay**. The results should be interpreted with caution and are not a substitute for medical advice 
    or clinical diagnostics. Please consult a healthcare professional for proper evaluation.
    """)

except Exception as e:
    st.error(f'An error occurred: {str(e)}')
    st.info('Please make sure all model files are properly loaded and try again.')
