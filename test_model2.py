import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

models_to_test = [
    "gemini-2.0-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemma-4-26b-a4b-it",
    "gemini-3.6-flash"
]

for model_name in models_to_test:
    print(f"Testing {model_name}...")
    try:
        response = client.models.generate_content(
            model=model_name,
            contents="Hola"
        )
        print(f"Success for {model_name}: {response.text[:20]}...")
        break # Found one that works!
    except Exception as e:
        print(f"Failed for {model_name}: {e}")
    time.sleep(1)

