import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

models_to_test = [
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-002",
    "gemini-1.5-pro-001",
    "gemini-1.5-pro-002",
    "gemini-2.0-flash-exp"
]

for model_name in models_to_test:
    print(f"Testing {model_name}...")
    try:
        response = client.models.generate_content(
            model=model_name,
            contents="Hola"
        )
        print(f"Success for {model_name}: {response.text[:20]}...")
    except Exception as e:
        print(f"Failed for {model_name}: {e}")

