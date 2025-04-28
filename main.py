import os
from cleaner.file_converter import convert_file
from cleaner.markdown_cleaner import clean_markdown

HEADER_FOOTER_PATTERNS = [
    r'^Page\s+\d+\s*$',
    r'^.*\.pdf\s*$',
    r'^Chapter\s+\d+\s*$',
]

INPUT_FOLDER = "example/"
CONVERTED_FOLDER = "output/converted/"
CLEANED_FOLDER = "output/cleaned/"

SUPPORTED_EXTENSIONS = ['.pdf', '.doc', '.docx', '.txt']

def main():
    # Step 1: Convert all supported files to MD
    for root, dirs, files in os.walk(INPUT_FOLDER):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, INPUT_FOLDER)
                output_path = os.path.join(CONVERTED_FOLDER, os.path.splitext(relative_path)[0] + '.md')
                convert_file(input_path, output_path)
                print(f"Converted: {input_path} -> {output_path}")

    # Step 2: Clean all generated MD files
    for root, dirs, files in os.walk(CONVERTED_FOLDER):
        for file in files:
            if file.endswith('.md'):
                input_path = os.path.join(root, file)
                with open(input_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                cleaned_content = clean_markdown(content, HEADER_FOOTER_PATTERNS)

                relative_path = os.path.relpath(input_path, CONVERTED_FOLDER)
                cleaned_path = os.path.join(CLEANED_FOLDER, relative_path)
                os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)

                with open(cleaned_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                
                print(f"Cleaned: {input_path} -> {cleaned_path}")

if __name__ == "__main__":
    main()
