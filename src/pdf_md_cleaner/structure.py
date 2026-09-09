import re
from typing import List


def is_rule_heading(line: str) -> bool:
    """Check if a line matches rule heading patterns like 'Rule 1. General'."""
    text = line.strip()
    if not text:
        return False
    return bool(re.match(r"^Rule\s+\d+[\.\:]?\s*.*$", text, flags=re.IGNORECASE))


def is_numbered_heading(line: str) -> bool:
    """Check if a line matches numbered patterns like '1.1 Definitions' or '2.3.1 Scope'."""
    text = line.strip()
    if not text:
        return False
    return bool(re.match(r"^\d+(?:\.\d+)+\.?\s+[A-Za-z0-9].*$", text))


def is_heading(line: str) -> bool:
    """Check if a line matches any recognized document heading structure."""
    text = line.strip()
    if not text:
        return False

    if is_rule_heading(text):
        return True

    if is_numbered_heading(text):
        return True

    # Chapter / Part / Section markers: 'CHAPTER — I', 'PART II', 'SECTION 3'
    if re.match(r"^(?:CHAPTER|PART|SECTION)\s*[-—:]?\s*[IVXLCDM0-9]+.*$", text, flags=re.IGNORECASE):
        return True

    # Short uppercase headers: 'PREFACE', 'GENERAL', 'ANNEXURE I'
    letters = [c for c in text if c.isalpha()]
    if letters and text.isupper() and len(text.split()) <= 6 and len(text) >= 3:
        return True

    return False


def extract_headings(text: str) -> List[str]:
    """Extract all recognized heading lines from a block of text."""
    headings: List[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if is_heading(line):
            headings.append(line)
    return headings
