import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from database import get_active_agent

# Load environment variables
load_dotenv()

# Check if the API key is set
api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

if api_key and api_key != "tu_api_key_aqui":
    client = genai.Client(api_key=api_key)
else:
    client = None

def get_chat_session(history=[]):
    """
    Initializes a chat session with the active agent's persona.
    """
    if not client:
        return None, "API Key no configurada"

    agent = get_active_agent()
    system_instruction = "Eres un asistente amigable."
    if agent:
        system_instruction = agent["persona"]

    try:
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
        )
        chat_session = client.chats.create(
            model=model_name,
            config=config
        )
        return chat_session, None
    except Exception as e:
        return None, str(e)

def send_message(chat_session, message):
    """
    Sends a message to the chat session and returns the response.
    """
    try:
        response = chat_session.send_message(message)
        return response.text
    except Exception as e:
        return f"Error al comunicarse con el modelo: {e}"
