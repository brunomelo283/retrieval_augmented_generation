import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


class LlamaClient:
    def __init__(
        self,
        model: str = "llama-3.3-70b-versatile",
        temperature: float = 0.0,
        max_tokens: int = 512
    ):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY não encontrada no .env!")

        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_completion_tokens": self.max_tokens,
            "temperature": self.temperature
        }

        response = requests.post(
            GROQ_API_URL,
            json=payload,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"].strip()
