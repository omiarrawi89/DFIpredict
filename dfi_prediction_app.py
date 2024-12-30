import streamlit as st
import numpy as np
import pickle

# Page config
st.set_page_config(
    page_title="Sperm DF% Prediction Tool",
    page_icon="🧬",
    layout="wide"
)

# Custom CSS to style the input fields and add tooltips next to them
st.markdown("""
<style>
input, .stNumberInput input {
    width: 200px !important;  /* Adjust width of input fields */
    height: 30px !important;  /* Adjust height of input fields */
    background-color: rgba(128, 0, 128, 0.1) !important; /* Transparent purple */
    border-radius: 8px !important;
    font-size: 16px !important;
}

.stTextInput input {
    width: 200px !important;  /* Adjust width of text input fields */
}

div.stNumberInput > div {
    width: 200px !important;  /* Adjust width for number input */
}

div.stButton > button {
    background-color: rgba(128, 0, 128, 0.7) !important;
    color: white !important;
}

h1, h2, h3, h4, h5, h6 {
    color: white !important;
}

.stTextInput, .stNumberInput {
    margin: 5px 0 !important;
}

.tooltip {
    position: absolute;
    top: 0;
    right: 0;
    border-radius: 50%;
    background-color: white;
    color: black;
    width: 20px;
    height: 20px;
    text-align: center;
    line-height: 20px;
    font-weight: bold;
    cursor: pointer;
    z-index: 10;
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 200px;
    background-color: rgba(128, 0, 128, 0.7);
    color: white;
    text-align: center;
    border-radius: 6px;
    padding: 5px;
    position: absolute;
    z-index: 1;
    bottom: 125%; /* Position above the text */
    left: 50%;
    margin-left: -100px;
    opacity: 0;
    transition: opacity 0.3s;
}

.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
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
    The model uses the following DF% ranges, as referenced from the study **10.1016/j.fertnstert.2004.07.115**:
    - **DF% < 15%**: Excellent fertility potential
    - **15% ≤ DF% < 25%**: Moderate fertility impact
    - **DF% ≥ 25%**: High fertility impact
    """)

    # Input parameters section with hover tooltips
    st.subheader('Input Parameters')

    # Progressive Motility
    progressive = st.number_input(
        '🚀 Progressive Motility (%)  ',
        0.0, 100.0, 50.0, 0.1,
    )
    st.markdown('<div class="tooltip" title="Progressive motility typically falls between 30-70%. Higher motility indicates better sperm movement.">❓<span class="tooltiptext">Progressive motility typically falls between 30-70%. Higher motility indicates better sperm movement.</span></div>', unsafe_allow_html=True)

    # Non-Progressive Motility
    non_progressive = st.number_input(
        '🐢 Non-Progressive Motility (%)  ',
        0.0, 100.0, 10.0, 0.1,
    )
    st.markdown('<div class="tooltip" title="Non-progressive motility usually ranges between 5-20%. It refers to sperm that moves but not effectively.">❓<span class="tooltiptext">Non-progressive motility usually ranges between 5-20%. It refers to sperm that moves but not effectively.</span></div>', unsafe_allow_html=True)

    # Immotile Sperm
    immotile = st.number_input(
        '🛑 Immotile Sperm (%)  ',
        0.0, 100.0, 40.0, 0.1,
    )
    st.markdown('<div class="tooltip" title="Immotile sperm are typically 30-60%. These sperm do not move.">❓<span class="tooltiptext">Immotile sperm are typically 30-60%. These sperm do not move.</span></div>', unsafe_allow_html=True)

    # Sperm Concentration
    concentration = st.number_input(
        '🔬 Sperm Concentration (million/mL)  ',
        0.0, 300.0, 50.0, 0.1,
    )
    st.markdown('<div class="tooltip" title="Sperm concentration is usually between 15-100 million sperm per mL.">❓<span class="tooltiptext">Sperm concentration is usually between 15-100 million sperm per mL.</span></div>', unsafe_allow_html=True)

    # Normal Morphology
    normal_sperm = st.number_input(
        '🌟 Normal Morphology (%)  ',
        0.0, 100.0, 14.0, 0.1,
    )
    st.markdown('<div class="tooltip" title="Normal sperm morphology is typically between 4-14%.">❓<span class="tooltiptext">Normal sperm morphology is typically between 4-14%.</span></div>', unsafe_allow_html=True)

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
    or clinical diagnostics. Please consult a healthcare professional for proper evaluation.
    """)

except Exception as e:
    st.error(f'An error occurred: {str(e)}')
    st.info('Please make sure all model files are properly loaded and try again.')
