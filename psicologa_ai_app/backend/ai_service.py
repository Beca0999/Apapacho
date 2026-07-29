import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class PsychologyAgent:
    def __init__(self, system_prompt: str):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "tu_api_key_aqui":
            raise ValueError("La API Key de Gemini no está configurada correctamente en el archivo .env")
        
        genai.configure(api_key=api_key)
        
        # Uso de un modelo recomendado para interacciones conversacionales
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_prompt
        )
        self.chat = self.model.start_chat(history=[])

    def send_message(self, message: str) -> str:
        """Envía un mensaje al agente y retorna la respuesta."""
        response = self.chat.send_message(message)
        return response.text
