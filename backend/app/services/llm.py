import requests


OLLAMA_URL = "http://localhost:11434/api/chat"


def ask_llm(prompt: str):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "qwen2.5:1.5b",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }
    )

    data = response.json()

    return data["message"]["content"]