import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY", "AIzaSyBYX9p_je2jU7yTB9q3qDa-cxGsIOM7Pc4"))
MODEL_NAME = "models/gemini-2.5-flash"

def call_gemini(prompt: str) -> str:
    # for model in genai.list_models():
    #     print(model.name, model.supported_generation_methods)
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt) # .md format
    return response.text or "(no response 🥺)"
