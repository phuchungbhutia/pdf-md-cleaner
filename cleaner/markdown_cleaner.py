import re

def remove_page_headers_footers(text, patterns):
    for pattern in patterns:
        text = re.sub(pattern, '', text, flags=re.MULTILINE)
    return text

def fix_broken_paragraphs(text):
    # Merge lines unless they end with punctuation
    return re.sub(r'(?<![\.\?\!\:])\n(?![\n#\-\*])', ' ', text)

def convert_all_caps_to_headings(text):
    def repl(match):
        heading = match.group(1).title()
        return f"\n## {heading}\n"
    return re.sub(r'^\s*([A-Z][A-Z\s]{3,})$', repl, text, flags=re.MULTILINE)

def clean_markdown(content, patterns):
    content = remove_page_headers_footers(content, patterns)
    content = fix_broken_paragraphs(content)
    content = convert_all_caps_to_headings(content)
    return content
