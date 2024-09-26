from flask import Flask, request, jsonify
import fitz  # PyMuPDF library for PDF
from docx import Document  # python-docx library for Word
import os

app = Flask(__name__)

def detect_file_type(file_path):
    _, file_extension = os.path.splitext(file_path.lower())
    if file_extension == '.pdf':
        return 'pdf'
    elif file_extension == '.docx':
        return 'docx'
    else:
        raise ValueError("Unsupported file type")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()

    return text

def extract_text_from_word(docx_path):
    doc = Document(docx_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + " "

    return text

def clean_text(text):
    # Remove line breaks and hyphens
    cleaned_text = text.replace("\n", " ").replace("- ", "")
    return cleaned_text

@app.route('/')
def index():
    message = "Welcome to the Text extractor API!"
    # Check if the request is a GET request
    if request.method == 'GET':
        message += " Developed by - SAHITYA KARAHE"

    return message

@app.route('/extract_text', methods=['POST'])
def extract_text():
    try:
        file = request.files['file']
        file.save('uploaded_file' + os.path.splitext(file.filename)[1])

        file_path = 'uploaded_file' + os.path.splitext(file.filename)[1]
        file_type = detect_file_type(file_path)

        if file_type == 'pdf':
            text = extract_text_from_pdf(file_path)
        elif file_type == 'docx':
            text = extract_text_from_word(file_path)
        else:
            return jsonify({"error": "Unsupported file type"})

        cleaned_text = clean_text(text)
        return jsonify({"cleaned_text": cleaned_text})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)), host='0.0.0.0', debug=True)
