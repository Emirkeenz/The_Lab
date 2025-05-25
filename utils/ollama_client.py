import requests
import logging

OLLAMA_SERVER_IP = "127.0.0.1"
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
        return response.json().get("response", "🤖 Не удалось получить ответ.")
    except Exception as e:
        logging.error(f"Ollama error: {e}")
        return "❌ Ошибка при запросе к модели."

def summarize_text(text: str) -> str:
    prompt = f"Сделай краткое саммари следующего урока:\n\n{text}"
    return query_ollama(prompt)

def explain_text(text: str) -> str:
    prompt = f"Объясни проще следующий текст:\n\n{text}"
    return query_ollama(prompt)
