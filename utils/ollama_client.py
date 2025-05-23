import requests
import logging

OLLAMA_SERVER_IP = "127.0.0.1"  # твой IP
OLLAMA_PORT = 11434
OLLAMA_URL = f"http://{OLLAMA_SERVER_IP}:{OLLAMA_PORT}/api/generate"

def query_ollama(prompt: str, model: str = "mistral") -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result.get("response", "Извините, модель не смогла ответить.")
    except Exception as e:
        logging.error(f"Ошибка запроса к Ollama: {e}")
        return "Ошибка при общении с AI-моделью."
