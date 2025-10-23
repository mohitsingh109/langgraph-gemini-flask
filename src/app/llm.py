import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY", "AIzaSyBYX9p_je2jU7yTB9q3qDa-cxGsIOM7Pc4"))
def call_gemini(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-1.0-pro")
    response = model.generate_content(prompt)
    return response.text or "(no response 🥺)"
