# core/llama.py

import requests

def ask_llama(context, question):
    url = "http://localhost:11434/api/generate"

    # Build the prompt based on whether context exists
    if context.strip():
        prompt = f"""Use the document below to answer the user's question.

Document:
{context.strip()}

Question: {question.strip()}
Answer:"""
    else:
        prompt = f"""Answer the following question.

Question: {question.strip()}
Answer:"""

    try:
        response = requests.post(url, json={
            "model": "llama2",     # ✅ ensure this matches your model
            "prompt": prompt,
            "stream": False
        })

        if response.status_code != 200:
            print(f"[LLAMA ERROR] Status {response.status_code}: {response.text}")
            return "⚠️ AI model failed to respond properly."

        data = response.json()

        return data.get("response", "").strip() or "⚠️ No answer generated."

    except requests.exceptions.ConnectionError:
        print("[LLAMA ERROR] Cannot connect to Ollama server at http://localhost:11434")
        return "⚠️ Ollama server is not running. Please start it using `ollama serve` or `ollama run llama2`."

    except Exception as e:
        print(f"[LLAMA ERROR] Unexpected: {str(e)}")
        return "⚠️ An unexpected error occurred while querying the AI model."
