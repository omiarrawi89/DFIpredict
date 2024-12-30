import streamlit as st
import numpy as np
import pickle

# Page config
st.set_page_config(
    page_title="Sperm DF% Prediction Tool",
    page_icon="🧬",
    layout="wide"
)

# Custom CSS for setting input styles and transparent background
st.markdown("""
<style>
input {
    height: 30px !important;
    background-color: rgba(128, 0, 128, 0.1) !important; /* Transparent purple */
    border-radius: 8px !important;
    font-size: 16px !important;
}

h1, h2, h3, h4, h5, h6 {
    color: white !important;
}

div.stButton > button {
    background-color: rgba(128, 0, 128, 0.7) !important;
    color: white !important;
}

.stTextInput input {
    background-color: rgba(128, 0, 128, 0.1) !important;
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
    Predict the **DNA Fragmentation Percentage (DF%)** of sperm based on **progressive motility**, **non-progressive motility**, **immotile sperm**, **sperm concentration**, and **normal morphology**, using an ensemble of **Gradient Boosting**, **Random Forest**, and **Neural Network** techniques.
    """)

    # Input parameters section
    st.subheader('Input Parameters')
    progressive = st.number_input('🚀 Progressive Motility (%)', 0.0, 100.0, 50.0, 0.1, help="Typically 30-70%")
    non_progressive = st.number_input('🐢 Non-Progressive Motility (%)', 0.0, 100.0, 10.0, 0.1, help="Typically 5-20%")
    immotile = st.number_input('🛑 Immotile Sperm (%)', 0.0, 100.0, 40.0, 0.1, help="Typically 30-60%")
    concentration = st.number_input('🔬 Sperm Concentration (million/mL)', 0.0, 300.0, 50.0, 0.1, help="Typically 15-100 million/mL")
    normal_sperm = st.number_input('🌟 Normal Morphology (%)', 0.0, 100.0, 14.0, 0.1, help="Typically 4-14%")

    # Validate input consistency
    if progressive + non_progressive + immotile != 100:
        st.warning("The sum of motility percentages (Progressive, Non-Progressive, Immotile) should equal 100%.")
    
    # Add prediction button
    if st.button('Predict DF%'):
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

        # Dynamic feedback
        if concentration < 15:
            st.info("Concentration is below the typical threshold (15 million/mL). Consider further analysis.")
        if normal_sperm < 4:
            st.warning("Normal Morphology is critically low (<4%). This may indicate a higher likelihood of DNA fragmentation.")

    # Disclaimer
    st.markdown('---')
    st.markdown("""
    **Disclaimer**: This DF% prediction tool is not a diagnostic tool. It is based on a model built using **limited training data** 
    and the **chromatin dispersion assay**. The results should be interpreted with caution and are not a substitute for medical advice 
    or clinical diagnostics. Please consult a healthcare professional for proper e
