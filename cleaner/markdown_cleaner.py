import os
import re


def clean_markdown_content(content: str) -> str:
    # Remove page numbers like "Page 1", "Page 23"
    content = re.sub(r"\n?Page\s+\d+\n?", "\n", content, flags=re.IGNORECASE)

    # Remove any repeated header/footer text across pages
    repeated_patterns = [
        r"^\s*Chapter\s+\d+.*$",  # Example: "Chapter 1 Introduction" repeated
        r"^\s*Document Title.*$",  # Example: "Document Title" repeated
    ]
    for pattern in repeated_patterns:
        content = re.sub(pattern, "", content, flags=re.MULTILINE | re.IGNORECASE)

    # Fix headings spacing: ensure space after # in heading
    content = re.sub(r"^(#+)([^\s#])", r"\1 \2", content, flags=re.MULTILINE)

    # Fix multiple newlines (>2) into exactly two
    content = re.sub(r"\n{3,}", "\n\n", content)

    # Clean excessive spaces (but careful not to break tables)
    def smart_space_clean(line):
        if line.strip().startswith("|") and line.strip().endswith("|"):
            return line  # likely a table line, don't touch
        return re.sub(r" {2,}", " ", line)

    content = "\n".join([smart_space_clean(line) for line in content.splitlines()])

    # Trim spaces at start and end
    content = content.strip()

    return content


def clean_markdown_file(file_path: str):
    """Clean a single markdown (.md) file"""
    print(f"🧹 Cleaning: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    cleaned_content = clean_markdown_content(content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(cleaned_content)


def clean_markdown_folder(folder_path: str):
    """Recursively clean all markdown files in a folder"""
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                clean_markdown_file(file_path)
