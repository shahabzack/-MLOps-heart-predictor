import streamlit as st
import requests

st.set_page_config(page_title="Heart Disease Predictor", layout="centered")
st.title("💓 Heart Disease Prediction App")

st.markdown("Enter patient details below to predict heart disease risk.")

# Collect input
age = st.number_input("Age", min_value=1, max_value=120, value=60)

sex = st.selectbox("Sex", options=[0, 1], format_func=lambda x: "Female" if x == 0 else "Male")

cp = st.selectbox("Chest Pain Type", options=[0, 1, 2, 3], format_func=lambda x: [
    "Typical Angina",
    "Atypical Angina",
    "Non-anginal Pain",
    "Asymptomatic"
][x])

trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=80, max_value=200, value=130)

chol = st.number_input("Serum Cholesterol (mg/dl)", min_value=100, max_value=600, value=250)

fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")

restecg = st.selectbox("Resting ECG Results", options=[0, 1, 2], format_func=lambda x: [
    "Normal",
    "ST-T Abnormality",
    "Left Ventricular Hypertrophy"
][x])

thalach = st.number_input("Maximum Heart Rate Achieved", min_value=60, max_value=220, value=150)

exang = st.selectbox("Exercise Induced Angina", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")

oldpeak = st.number_input("ST Depression (Oldpeak)", min_value=0.0, max_value=10.0, step=0.1, value=1.0)

slope = st.selectbox("Slope of Peak Exercise ST Segment", options=[0, 1, 2], format_func=lambda x: [
    "Upsloping",
    "Flat",
    "Downsloping"
][x])

ca = st.selectbox("Number of Major Vessels Colored (0-3)", options=[0, 1, 2, 3])

thal = st.selectbox(
    "Thalassemia Test Result",
    options=[1, 2, 3],
    format_func=lambda x: {
        1: "Normal",
        2: "Fixed Defect",
        3: "Reversible Defect"
    }.get(x, "Unknown")
)


# Send data
if st.button("Predict"):
    input_data = {
        "age": age,
        "sex": sex,
        "cp": cp,
        "trestbps": trestbps,
        "chol": chol,
        "fbs": fbs,
        "restecg": restecg,
        "thalach": thalach,
        "exang": exang,
        "oldpeak": oldpeak,
        "slope": slope,
        "ca": ca,
        "thal": thal
    }

    try: # render hosted fast api link
        res = requests.post("https://fastapi-mlops-4yyq.onrender.com/predict", json=input_data) 
        if res.status_code == 200:
            result = res.json()
            st.success(f"🩺 Prediction: **{result['prediction']}**")
            st.info(f"Confidence: **{result['confidence']}%**")
        else:
            st.error(f"Error: {res.text}")
    except Exception as e:
        st.error(f"Failed to connect to API: {e}")
