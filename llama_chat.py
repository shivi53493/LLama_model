import requests

def ask_llama(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama2",  # or llama3, etc.
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()['response'].strip()
    except Exception as e:
        return f"❌ Error: {e}"


# 🧪 Test the model
if __name__ == "__main__":
    print("🤖 LLaMA Chat (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        reply = ask_llama(user_input)
        print("LLaMA:", reply)
