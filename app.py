import streamlit as st
import joblib
import pandas as pd
from recommendation import get_crop_recommendation

# Load model
data = joblib.load("model.pkl")
model = data["model"]
accuracy = data["accuracy"]

# UI
st.title("🌱 Smart Agriculture AI System")

st.write("Enter soil and weather details to get the best crop recommendation.")

# Show model accuracy
st.info(f"📊 Model Accuracy: {accuracy * 100:.2f}%")

# Inputs
N = st.number_input("Nitrogen (N)", 0, 200)
P = st.number_input("Phosphorus (P)", 0, 200)
K = st.number_input("Potassium (K)", 0, 200)
temp = st.number_input("Temperature (°C)", 0.0, 50.0)
humidity = st.number_input("Humidity (%)", 0.0, 100.0)
ph = st.number_input("Soil pH", 0.0, 14.0)
rainfall = st.number_input("Rainfall (mm)", 0.0, 500.0)

if st.button("Predict Crop"):
    input_data = pd.DataFrame(
        [[N, P, K, temp, humidity, ph, rainfall]],
        columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    )

    prediction = model.predict(input_data)[0]

    result = get_crop_recommendation(prediction)

    st.success(result)
