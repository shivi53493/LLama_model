import os
from flask import Flask, request, render_template, jsonify
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import docx
import requests

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Utility: Extract text based on file type
def extract_text(file_path):
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        return " ".join([page.extract_text() for page in reader.pages])
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return " ".join([p.text for p in doc.paragraphs])
    elif file_path.lower().endswith((".png", ".jpg", ".jpeg")):
        img = Image.open(file_path)
        return pytesseract.image_to_string(img)
    else:
        return "Unsupported file type."

# LLaMA call
def ask_llama(context, question):
    url = "http://localhost:11434/api/generate"
    prompt = f"""Use the document below to answer the user's question.

Document:
{context}

Question: {question}
Answer:"""

    payload = {
        "model": "llama2",
        "prompt": prompt,
        "stream": False
    }

    res = requests.post(url, json=payload)
    return res.json()['response'].strip()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    extracted_text = extract_text(file_path)
    return jsonify({"text": extracted_text})


@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    context = data.get("context", "")
    question = data.get("question", "")
    answer = ask_llama(context, question)
    return jsonify({"answer": answer})


if __name__ == '__main__':
    app.run(debug=True)
