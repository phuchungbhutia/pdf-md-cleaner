import re
from typing import List


def is_rule_heading(line: str) -> bool:
    """Check if line matches rule heading patterns like 'Rule 1. General'."""
    text = line.strip()
    if not text:
        return False
    return bool(
        re.match(r"^Rule\s+\d+[\.\:]?\s*.*$", text, flags=re.IGNORECASE)
    )


def is_numbered_heading(line: str) -> bool:
    """Check if line matches numbered patterns like '1.1 Definitions'."""
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

    chapter_pattern = (
        r"^(?:CHAPTER|PART|SECTION)\s*[-—:]?\s*[IVXLCDM0-9]+.*$"
    )
    if re.match(chapter_pattern, text, flags=re.IGNORECASE):
        return True

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


def markdownize_structure(text: str) -> str:
    """Convert recognized document headings into standard Markdown headings."""
    output_lines: List[str] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            output_lines.append("")
            continue

        if line.startswith("#"):
            output_lines.append(line)
            continue

        chapter_pattern = (
            r"^(?:CHAPTER|PART)\s*[-—:]?\s*[IVXLCDM0-9]+.*$"
        )
        if re.match(chapter_pattern, line, flags=re.IGNORECASE):
            output_lines.append(f"## {line}")
        elif is_rule_heading(line) or is_numbered_heading(line):
            output_lines.append(f"### {line}")
        elif is_heading(line):
            output_lines.append(f"## {line}")
        else:
            output_lines.append(raw_line)

    return "\n".join(output_lines)
