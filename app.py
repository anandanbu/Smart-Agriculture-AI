import streamlit as st
import joblib
import pandas as pd
from recommendation import get_crop_recommendation
from grok_chatbot import GrokChatbot
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Grok chatbot
grok = GrokChatbot()

# Load model
data = joblib.load("model.pkl")
model = data["model"]
accuracy = data["accuracy"]

# UI
st.set_page_config(page_title="🌱 Smart Agriculture AI", layout="wide")
st.title("🌱 Smart Agriculture AI System")

st.write("Intelligent crop recommendations with AI-powered insights and farming advice")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["🌾 Crop Prediction", "💡 AI Insights", "🤖 Farming Assistant", "📚 Disease Prevention"]
)

# ============= TAB 1: CROP PREDICTION =============
with tab1:
    st.subheader("Crop Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Soil Parameters**")
        N = st.number_input("Nitrogen (N) mg/kg", 0, 200, value=50)
        P = st.number_input("Phosphorus (P) mg/kg", 0, 200, value=50)
        K = st.number_input("Potassium (K) mg/kg", 0, 200, value=50)
    
    with col2:
        st.write("**Weather Parameters**")
        temp = st.number_input("Temperature (°C)", 0.0, 50.0, value=25.0)
        humidity = st.number_input("Humidity (%)", 0.0, 100.0, value=60.0)
        ph = st.number_input("Soil pH", 0.0, 14.0, value=6.5)
        rainfall = st.number_input("Rainfall (mm)", 0.0, 500.0, value=100.0)
    
    st.info(f"📊 Model Accuracy: {accuracy * 100:.2f}%")
    
    if st.button("🔮 Predict Best Crop", use_container_width=True):
        input_data = pd.DataFrame(
            [[N, P, K, temp, humidity, ph, rainfall]],
            columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        )
        
        prediction = model.predict(input_data)[0]
        result = get_crop_recommendation(prediction)
        
        st.success(result)
        st.session_state.last_prediction = prediction
        st.session_state.last_params = {
            'N': N, 'P': P, 'K': K, 'temp': temp,
            'humidity': humidity, 'ph': ph, 'rainfall': rainfall
        }

# ============= TAB 2: AI INSIGHTS =============
with tab2:
    st.subheader("AI-Powered Insights with Grok")
    
    if 'last_prediction' in st.session_state:
        if st.button("📊 Get Detailed Insights for Last Prediction", use_container_width=True):
            with st.spinner("🔄 Grok is analyzing your farm conditions..."):
                params = st.session_state.last_params
                insights = grok.get_crop_insights(
                    st.session_state.last_prediction,
                    params['N'], params['P'], params['K'],
                    params['temp'], params['humidity'],
                    params['ph'], params['rainfall']
                )
                st.markdown(insights)
    else:
        st.info("💡 First, make a crop prediction in the 'Crop Prediction' tab to get insights")

# ============= TAB 3: FARMING ASSISTANT =============
with tab3:
    st.subheader("🤖 AI Farming Assistant")
    
    st.write("Ask any farming-related questions and get expert advice from Grok AI")
    
    question = st.text_area(
        "Your farming question:",
        placeholder="e.g., How do I improve soil fertility? What's the best time to plant wheat?",
        height=100
    )
    
    if st.button("💬 Get Expert Advice", use_container_width=True):
        if question.strip():
            with st.spinner("🤔 Thinking..."):
                response = grok.get_farming_advice(question)
                st.markdown(response)
        else:
            st.warning("Please enter a question")
    
    # Chat history
    st.divider()
    st.subheader("💬 Quick Questions")
    
    quick_questions = [
        "How to increase crop yield naturally?",
        "What's the best irrigation method for my area?",
        "How do I manage pests organically?",
        "What crops can I grow in monsoon season?",
        "How to improve soil pH naturally?"
    ]
    
    cols = st.columns(2)
    for idx, q in enumerate(quick_questions):
        with cols[idx % 2]:
            if st.button(q, key=f"quick_{idx}", use_container_width=True):
                with st.spinner("⏳ Getting response..."):
                    response = grok.get_farming_advice(q)
                    st.markdown(response)

# ============= TAB 4: DISEASE PREVENTION =============
with tab4:
    st.subheader("🛡️ Disease Prevention Guide")
    
    crops = ["rice", "wheat", "maize", "cotton", "sugarcane"]
    selected_crop = st.selectbox("Select crop for disease prevention tips:", crops)
    
    if st.button(f"📚 Get Prevention Tips for {selected_crop.title()}", use_container_width=True):
        with st.spinner(f"🔍 Fetching disease prevention tips for {selected_crop}..."):
            tips = grok.get_disease_prevention_tips(selected_crop)
            st.markdown(tips)

# ============= FOOTER =============
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🤖 Powered by Grok AI")
with col2:
    st.caption("📊 ML Model: Random Forest")
with col3:
    st.caption("🌍 For Smart Farming")
