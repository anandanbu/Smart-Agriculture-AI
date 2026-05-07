import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class GroqChatbot:
    def __init__(self, api_key=None):
        """Initialize Groq API chatbot"""

        self.api_key = (
            api_key
            or os.getenv("GROQ_API_KEY")
            or st.secrets.get("GROQ_API_KEY")
        )

        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

        self.model = "llama-3.3-70b-versatile"

    def get_crop_insights(self, crop, N, P, K, temp, humidity, ph, rainfall):
        """Get detailed insights about crop and soil conditions from Groq"""

        prompt = f"""
Based on the following soil and weather parameters for growing {crop}:
- Nitrogen (N): {N} mg/kg
- Phosphorus (P): {P} mg/kg
- Potassium (K): {K} mg/kg
- Temperature: {temp}°C
- Humidity: {humidity}%
- Soil pH: {ph}
- Rainfall: {rainfall}mm

Provide:
1. Suitability assessment (is this ideal for {crop}?)
2. Key insights about the soil conditions
3. Weather compatibility analysis
4. 3-5 actionable recommendations for optimization
5. Potential challenges and solutions

Keep response concise and practical for a farmer.
"""

        return self._call_groq(prompt)

    def get_farming_advice(self, query):
        """Get general farming advice from Groq"""

        prompt = f"""As an expert agricultural advisor, answer the following farmer's question:

{query}

Provide practical, actionable advice specific to Indian agriculture.
Keep response concise and easy to understand."""

        return self._call_groq(prompt)

    def get_disease_prevention_tips(self, crop):
        """Get disease prevention tips for a specific crop"""

        prompt = f"""Provide the top 5 disease prevention measures for {crop} farming:

For each measure include:
- The disease it prevents
- Why it's important
- How to implement it

Use simple language suitable for farmers."""

        return self._call_groq(prompt)

    def _call_groq(self, prompt):
        """Internal method to call Groq API"""

        try:

            if not self.api_key:
                return "⚠️ Error: GROQ_API_KEY not found in environment variables. Please set it in your .env file."

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert agricultural advisor helping farmers with crop recommendations and farming practices."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }

            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=15
            )

            if response.status_code == 401:
                return "⚠️ Error: Invalid API Key. Please check your GROQ_API_KEY in .env file."

            elif response.status_code == 400:
                return f"⚠️ Bad Request: Check your API key and model name. Response: {response.text}"

            elif response.status_code != 200:
                return f"⚠️ API Error {response.status_code}: {response.text}"

            result = response.json()

            return result["choices"][0]["message"]["content"]

        except requests.exceptions.Timeout:
            return "⚠️ Request timeout. Please try again."

        except requests.exceptions.RequestException as e:
            return f"⚠️ Error connecting to Groq API: {str(e)}"

        except KeyError as e:
            return f"⚠️ Unexpected API response format: {str(e)}"

        except Exception as e:
            return f"⚠️ Error: {str(e)}"
