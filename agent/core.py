import requests
import json

url = "http://localhost:11434/api/generate"

def run_agent(message: list[dict]) -> str:
    """
    :param message: [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."},
        ...
    ]
    :return:
    """
    payload = {
        "model": "llama3",
        "prompt": message,
        "stream": False
    }
    response = requests.post(url, json=payload)
    data = response.json()

    # Ollama 返回格式：{"message": {"content": "..."}}
    return data["response"]
