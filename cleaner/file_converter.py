import os
import pathlib

import pdfplumber
import docx
import mammoth  # better .docx -> markdown converter

from markdownify import markdownify as md  # for html -> md conversion


def convert_pdf_to_md(input_path, output_path):
    md_text = ""
    with pdfplumber.open(input_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                md_text += text + "\n\n"
    md_text = md(md_text)  # Convert raw text to markdown
    save_markdown(md_text, input_path, output_path)


def convert_docx_to_md(input_path, output_path):
    with open(input_path, "rb") as docx_file:
        result = mammoth.convert_to_markdown(docx_file)
        md_text = result.value
    save_markdown(md_text, input_path, output_path)


def convert_txt_to_md(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    md_text = md(text)  # Convert plain text to markdown
    save_markdown(md_text, input_path, output_path)


def save_markdown(md_text, input_path, output_path):
    """Save converted markdown to output_path with .md extension"""
    filename = pathlib.Path(input_path).stem + ".md"
    output_file = os.path.join(output_path, filename)
    os.makedirs(output_path, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(md_text)
    print(f"✅ Saved: {output_file}")


def convert_files(input_folder="example", output_folder="output"):
    """Convert all supported files in input_folder to markdown"""
    supported_extensions = [".pdf", ".doc", ".docx", ".txt"]

    for root, _, files in os.walk(input_folder):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            input_path = os.path.join(root, file)

            if ext not in supported_extensions:
                continue

            relative_path = os.path.relpath(root, input_folder)
            output_path = os.path.join(output_folder, relative_path)

            print(f"📄 Converting: {input_path}")

            try:
                if ext == ".pdf":
                    convert_pdf_to_md(input_path, output_path)
                elif ext in [".doc", ".docx"]:
                    convert_docx_to_md(input_path, output_path)
                elif ext == ".txt":
                    convert_txt_to_md(input_path, output_path)
            except Exception as e:
                print(f"❌ Error converting {input_path}: {e}")
