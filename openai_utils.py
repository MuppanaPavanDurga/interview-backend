import os
import requests
from dotenv import load_dotenv

load_dotenv()

def format_chat(chat):
    return "\n".join([f"{c['sender']}: {c['text']}" for c in chat])

def generate_question(role, chat_history):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    # Format chat history
    def format_chat(chat):
        return "\n".join([f"{c['sender']}: {c['text']}" for c in chat])

    # 🔄 Different prompt depending on mode
    if role == "general":
        prompt = f"""You are a helpful AI assistant. Answer user queries in a friendly and concise manner.

Here is the conversation so far:
{format_chat(chat_history)}

Respond helpfully to the last user message."""
    else:
        prompt = f"""You are a senior technical interviewer for the role of {role}.
Your task is to ask one clear, concise technical interview question at a time.

If the user has already answered a question, provide structured feedback.

Here is the conversation so far:
{format_chat(chat_history)}

Respond with the next interview question or feedback.
"""

    data = {
        "model": "meta-llama/llama-3-8b-instruct",  # Or other available OpenRouter model
        "messages": [
            { "role": "user", "content": prompt }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"
