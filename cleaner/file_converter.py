import os
import fitz  # PyMuPDF
import docx
from markdownify import markdownify as md

def convert_pdf_to_md(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc)
    return md(text)

def convert_docx_to_md(docx_path):
    doc = docx.Document(docx_path)
    full_text = "\n".join([para.text for para in doc.paragraphs])
    return md(full_text)

def convert_txt_to_md(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return md(text)

def convert_file(input_path, output_path):
    ext = os.path.splitext(input_path)[1].lower()
    if ext == '.pdf':
        content = convert_pdf_to_md(input_path)
    elif ext == '.docx' or ext == '.doc':
        content = convert_docx_to_md(input_path)
    elif ext == '.txt':
        content = convert_txt_to_md(input_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
