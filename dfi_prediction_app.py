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
    This tool predicts the **DNA Fragmentation Percentage (DF%)** of sperm based on motility and morphology parameters.
    It leverages an ensemble model combining Gradient Boosting, Random Forest, and Neural Network techniques.
    """)

    st.markdown("""
    **Inputs Explained**:
    - The model uses **five key features**: progressive motility, non-progressive motility, immotile percentage, sperm concentration, and normal sperm morphology.
    - "Concentration" is included as it reflects the sperm count in a sample, which can influence DNA fragmentation levels.
    """)

    # Input parameters section with emojis and helper text
    st.subheader('Input Parameters (Required)')
    progressive = st.number_input('🚀 Progressive Motility (%)', 0.0, 100.0, 50.0, 0.1, help="Typically 30-70%")
    non_progressive = st.number_input('🐢 Non-Progressive Motility (%)', 0.0, 100.0, 10.0, 0.1, help="Typically 5-20%")
    immotile = st.number_input('🛑 Immotile Sperm (%)', 0.0, 100.0, 40.0, 0.1, help="Typically 30-60%")
    concentration = st.number_input('🔬 Sperm Concentration (million/mL)', 0.0, 300.0, 50.0, 0.1, help="Typically 15-100 million/mL")
    normal_sperm = st.number_input('🌟 Normal Morphology (%)', 0.0, 100.0, 14.0, 0.1, help="Typically 4-14%")

    # Add a predict button
    if st.button('Predict DF%', type='primary'):
        # Ensure input order matches model expectation
        input_features = np.array([[progressive, immotile, non_progressive, concentration, normal_sperm]])
        
        # Make prediction
        prediction = model.predict(input_features)[0]
        
        # Display results
        st.markdown('---')
        st.subheader('Prediction Results')
        
        # Determine result interpretation with emojis
        if prediction < 15:
            result = "🟢 Excellent fertility potential (DF% < 15%)"
            emoji = "😊"
        elif prediction < 25:
            result = "🟡 Moderate fertility impact (DF% 15-25%)"
            emoji = "😐"
        else:
            result = "🔴 High fertility impact (DF% > 25%)"
            emoji = "😟"
        
        # Display the result with DNA and sperm emojis
        st.metric(label="Predicted DF%", value=f"{prediction:.1f}% 🧬💦")
        st.write(f"Result: {result} {emoji}")
        
        # Add a colorful separator line
        st.markdown('---')
        st.subheader('Interpretation Guide')
        st.write("""
        - 🟢 **DF% < 15%**: Generally considered normal/good fertility potential.
        - 🟡 **DF% 15-25%**: Moderate fertility impact, may affect pregnancy outcomes.
        - 🔴 **DF% > 25%**: Higher impact on fertility, may indicate need for additional evaluation.
        """)
        st.markdown("""
        **Model Strengths**:
        - High accuracy in predicting normal (≤15%) and average (15-30%) ranges.
        - Consistent performance based on validation data.

        **Model Limitations**:
        - Tendency to overpredict average cases.
        - Reduced accuracy for high DF% values (≥30%).
        """)
    
    # Add Disclaimer at the bottom
    st.markdown('---')
    st.markdown("""
    **Disclaimer**: This DF% prediction tool is not a diagnostic tool. It is based on a model built using **limited training data** 
    and the **chromatin dispersion assay**. The results should be interpreted with caution and are not a substitute for medical advice 
    or clinical diagnostics. Please consult a healthcare professional for proper evaluation.
    """)

except Exception as e:
    st.error(f'An error occurred: {str(e)}')
    st.info('Please make sure all model files are properly loaded and try again.')
