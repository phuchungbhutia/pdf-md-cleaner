from cleaner.markdown_cleaner import clean_markdown

HEADER_FOOTER_PATTERNS = [
    r'^Page\s+\d+\s*$',                # Page numbers
    r'^.*YourFileName\.pdf\s*$',       # File name (adjust this)
    r'^Chapter\s+\d+\s*$',             # Chapter headers
]

def main():
    with open("example/sample.md", "r", encoding="utf-8") as f:
        content = f.read()

    cleaned = clean_markdown(content, HEADER_FOOTER_PATTERNS)

    with open("example/cleaned_sample.md", "w", encoding="utf-8") as f:
        f.write(cleaned)

if __name__ == "__main__":
    main()
