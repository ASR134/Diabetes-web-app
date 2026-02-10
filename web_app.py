import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="Diabetes Prediction",
    page_icon="🏥",
    layout="centered"
)

# Title and description
st.title("🏥 Diabetes Prediction System")
st.markdown("Enter your health parameters below to predict diabetes risk")

# API endpoint
API_URL = "https://diabetes-prediction-api-ekdt.onrender.com/predict"

# Create two columns for better layout
col1, col2 = st.columns(2)

with col1:
    pregnancies = st.number_input(
        "Number of Pregnancies",
        min_value=0,
        max_value=20,
        value=0,
        step=1,
        help="Number of times pregnant"
    )
    
    glucose = st.number_input(
        "Glucose Level (mg/dL)",
        min_value=1,
        max_value=300,
        value=100,
        step=1,
        help="Plasma glucose concentration"
    )
    
    blood_pressure = st.number_input(
        "Blood Pressure (mm Hg)",
        min_value=1,
        max_value=200,
        value=70,
        step=1,
        help="Diastolic blood pressure"
    )
    
    skin_thickness = st.number_input(
        "Skin Thickness (mm)",
        min_value=0,
        max_value=100,
        value=20,
        step=1,
        help="Triceps skin fold thickness"
    )

with col2:
    insulin = st.number_input(
        "Insulin Level (mu U/ml)",
        min_value=0,
        max_value=900,
        value=80,
        step=1,
        help="2-Hour serum insulin"
    )
    
    bmi = st.number_input(
        "BMI (Body Mass Index)",
        min_value=0.1,
        max_value=49.9,
        value=25.0,
        step=0.1,
        help="Body mass index (weight in kg/(height in m)^2)"
    )
    
    diabetes_pedigree = st.number_input(
        "Diabetes Pedigree Function",
        min_value=0.0,
        max_value=2.5,
        value=0.5,
        step=0.01,
        help="Diabetes pedigree function"
    )
    
    age = st.number_input(
        "Age (years)",
        min_value=1,
        max_value=119,
        value=25,
        step=1,
        help="Age in years"
    )

# Add some spacing
st.markdown("---")

# Prediction button
if st.button("🔍 Predict", type="primary", use_container_width=True):
    # Prepare data for API
    data = {
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BloodPressure": blood_pressure,
        "SkinThickness": skin_thickness,
        "Insulin": insulin,
        "BMI": bmi,
        "DiabetesPedigreeFunction": diabetes_pedigree,
        "Age": age
    }
    
    try:
        # Make API request
        with st.spinner("Making prediction..."):
            response = requests.post(API_URL, json=data)
        
        if response.status_code == 200:
            result = response.json()
            prediction_result = result.get("predicted category ", "Unknown")
            
            # Display result with styling
            st.markdown("### Prediction Result:")
            
            if prediction_result == "Non Diabetic":
                st.success(f"✅ {prediction_result}")
                st.balloons()
            else:
                st.error(f"⚠️ {prediction_result}")
            
            # Show input summary
            with st.expander("📊 View Input Summary"):
                st.json(data)
        else:
            st.error(f"Error: Received status code {response.status_code}")
            st.write(response.text)
            
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to the API. Please ensure the FastAPI server is running at http://127.0.0.1:8000")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Footer with instructions
st.markdown("---")
st.markdown("""
### 📝 Instructions:
1. Ensure the FastAPI server is running (`uvicorn main:app --reload`)
2. Enter your health parameters in the form above
3. Click the 'Predict' button to get your diabetes risk prediction

**Note:** This is a prediction tool and should not replace professional medical advice.
""")