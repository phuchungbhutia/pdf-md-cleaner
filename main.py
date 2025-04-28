# main.py

from cleaner.file_converter import convert_files
from cleaner.markdown_cleaner import clean_markdown_folder

def main():
    input_folder = "example"
    output_folder = "output"

    # Step 1: Convert supported files to Markdown
    print("🔄 Converting files to Markdown...")
    convert_files(input_folder, output_folder)

    # Step 2: Clean the generated Markdown files
    print("🧹 Cleaning Markdown files...")
    clean_markdown_folder(output_folder)

    print("✅ All done! Check the 'output/' folder.")


if __name__ == "__main__":
    main()
