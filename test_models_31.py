import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

for model_name in ["gemini-3.1-flash", "gemini-3.1-flash-lite"]:
    try:
        response = client.models.generate_content(
            model=model_name,
            contents="Hola"
        )
        print(f"Success for {model_name}: {response.text[:20]}...")
    except Exception as e:
        print(f"Failed for {model_name}: {e}")
