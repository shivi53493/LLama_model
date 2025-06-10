import os
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import docx
from pdf2image import convert_from_path  # <-- NEW
import pdfplumber
import shutil
# Update tesseract path if needed (Windows users)
tesseract_executable_path = shutil.which("tesseract")

def extract_text(file_path):
    ext = file_path.lower()

    if ext.endswith(".pdf"):
        try:
            with pdfplumber.open(file_path) as pdf:
                pages = pdf.pages
                text = ""
                for page in pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            return f"Error processing PDF: {str(e)}"

    elif ext.endswith(".txt"):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    elif ext.endswith(".docx"):
        doc = docx.Document(file_path)
        return " ".join([p.text for p in doc.paragraphs])

    elif ext.endswith((".png", ".jpg", ".jpeg")):
        img = Image.open(file_path)
        return pytesseract.image_to_string(img)

    return "Unsupported file type."
