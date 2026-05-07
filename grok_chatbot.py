import requests
import os
from dotenv import load_dotenv

load_dotenv()

class GrokChatbot:
    def __init__(self, api_key=None):
        """Initialize Grok API chatbot"""
        self.api_key = api_key or os.getenv("GROK_API_KEY")
        self.api_url = "https://api.x.ai/v1/chat/completions"
        self.model = "grok-beta"
        
    def get_crop_insights(self, crop, N, P, K, temp, humidity, ph, rainfall):
        """Get detailed insights about crop and soil conditions from Grok"""
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
        
        return self._call_grok(prompt)
    
    def get_farming_advice(self, query):
        """Get general farming advice from Grok"""
        prompt = f"""
        As an expert agricultural advisor, answer the following farmer's question:
        
        {query}
        
        Provide practical, actionable advice specific to Indian agriculture.
        Keep response concise and easy to understand.
        """
        
        return self._call_grok(prompt)
    
    def get_disease_prevention_tips(self, crop):
        """Get disease prevention tips for a specific crop"""
        prompt = f"""
        Provide the top 5 disease prevention measures for {crop} farming:
        
        For each measure include:
        - The disease it prevents
        - Why it's important
        - How to implement it
        
        Use simple language suitable for farmers.
        """
        
        return self._call_grok(prompt)
    
    def _call_grok(self, prompt):
        """Internal method to call Grok API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are an expert agricultural advisor helping farmers with crop recommendations and farming practices."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        
        except requests.exceptions.RequestException as e:
            return f"⚠️ Error connecting to Grok API: {str(e)}"
        except KeyError:
            return "⚠️ Unexpected API response format"
        except Exception as e:
            return f"⚠️ Error: {str(e)}"
