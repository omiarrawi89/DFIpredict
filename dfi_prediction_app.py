trimport streamlit as st
import numpy as np
import pickle
import matplotlib.pyplot as plt
from io import BytesIO
from fpdf import FPDF
import plotly.graph_objects as go

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
    
    # Sidebar Information
    st.sidebar.title("About the Tool")
    st.sidebar.info("""
    This tool predicts Sperm DNA Fragmentation Percentage (DF%) based on concentration, motility and morphology parameters.
    - Designed for educational purposes.
    - Not a substitute for medical diagnostics.
    """)
    
    # App title and description
    st.title('🧬 Sperm DNA Fragmentation Percentage Prediction Tool 💦')
    st.write("""
    Predict the **DNA Fragmentation Percentage (DF%)** of sperm using key parameters.
    The model leverages an ensemble of Gradient Boosting, Random Forest, and Neural Network techniques.
    """)

    # Input parameters section with emojis and helper text
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

        # Add a colorful separator line
        st.markdown('---')
        st.subheader('Graphs and Visualizations')
        
        # Bar chart of input parameters
        fig, ax = plt.subplots()
        labels = ['Progressive', 'Non-Progressive', 'Immotile', 'Concentration', 'Normal Morphology']
        values = [progressive, non_progressive, immotile, concentration, normal_sperm]
        ax.bar(labels, values, color=['blue', 'green', 'red', 'purple', 'orange'])
        ax.set_title('Input Parameters Overview')
        ax.set_ylabel('Value')
        st.pyplot(fig)
        
        # Radar chart
        categories = ['Progressive', 'Non-Progressive', 'Immotile', 'Concentration', 'Normal Morphology']
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Sperm Parameters'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            showlegend=True
        )
        st.plotly_chart(fig)

        # Add prediction history
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append({"Inputs": dict(zip(labels, values)), "DF%": prediction})

        st.subheader("Prediction History")
        if st.session_state.history:
            st.write(st.session_state.history)
        
        # Report generation
        def generate_report(inputs, prediction):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            # Title
            pdf.set_font("Arial", size=16, style='B')
            pdf.cell(200, 10, txt="Sperm DF% Prediction Report", ln=True, align='C')
            pdf.ln(10)
            
            # Inputs Section
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Inputs Provided:", ln=True)
            for key, value in inputs.items():
                pdf.cell(200, 10, txt=f"- {key}: {value}", ln=True)
            pdf.ln(10)
            
            # Prediction Section
            pdf.set_font("Arial", size=14, style='B')
            pdf.cell(200, 10, txt=f"Predicted DF%: {prediction:.1f}%", ln=True)
            pdf.ln(10)
            
            # Footer
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 10, txt="Disclaimer: This is not a diagnostic tool.", ln=True)
            
            buffer = BytesIO()
            pdf.output(buffer)
            buffer.seek(0)
            return buffer

        inputs = dict(zip(labels, values))
        buffer = generate_report(inputs, prediction)
        st.download_button(label="Download Report", data=buffer, file_name="df_prediction_report.pdf", mime="application/pdf")
    
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
