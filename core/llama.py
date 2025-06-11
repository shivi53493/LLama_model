# core/llama.py

import requests
import json
from markdown2 import markdown
from django.http import JsonResponse
def stream_llama_response(context, question):
    url = "http://localhost:11434/api/generate"

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
            # "model": "llama2",
            "model": "gemma3:1b-it-qat",
            "prompt": prompt,
            "stream": True
        }, stream=True)

        if response.status_code != 200:
            yield f"data: ⚠️ AI model error: {response.status_code}\n\n"
            return
        

        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    token = data.get("response", "")
                    
                    if token:
                        yield f"data: {token}\n\n"
                except Exception:
                    yield "data: ⚠️ Chunk parsing error\n\n"
       
        

    except requests.exceptions.ConnectionError:
        yield "data: ⚠️ Cannot connect to Ollama server.\n\n"

    except Exception as e:
        yield f"data: ⚠️ Unexpected error: {str(e)}\n\n"
