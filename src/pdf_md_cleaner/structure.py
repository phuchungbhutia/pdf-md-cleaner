import re


LEGAL_HEADING_PATTERNS = [
    r"^section\s+\d+",
    r"^chapter\s+[ivxlcdm\d]+",
    r"^part\s+[ivxlcdm\d]+",
    r"^rule\s+\d+",
    r"^regulation\s+\d+",
    r"^schedule\s+[ivxlcdm\d]+",
    r"^annexure\s+[a-z0-9]+",
    r"^appendix\s+[a-z0-9]+",
    r"^form\s+(no\.?\s*)?\d+",
]


def is_legal_heading(line: str) -> bool:

    normalized = line.strip().lower()

    for pattern in LEGAL_HEADING_PATTERNS:
        if re.match(pattern, normalized):
            return True

    return False


def is_numbered_heading(line: str) -> bool:

    return bool(
        re.match(
            r"^\d+(\.\d+)*[\.\)]?\s+\S+",
            line.strip(),
        )
    )


def is_all_caps_heading(line: str) -> bool:

    stripped = line.strip()

    if len(stripped) < 4:
        return False

    letters = [
        char
        for char in stripped
        if char.isalpha()
    ]

    if not letters:
        return False

    return (
        sum(char.isupper() for char in letters)
        / len(letters)
        >= 0.85
    )


def classify_heading(line: str) -> str | None:

    stripped = line.strip()

    if not stripped:
        return None

    if is_legal_heading(stripped):
        return "h2"

    if is_numbered_heading(stripped):
        return "h3"

    if is_all_caps_heading(stripped):
        return "h2"

    return None


def markdownize_structure(text: str) -> str:

    lines = text.splitlines()

    result = []

    for line in lines:

        heading = classify_heading(line)

        if heading == "h2":
            result.append(f"## {line.strip()}")

        elif heading == "h3":
            result.append(f"### {line.strip()}")

        else:
            result.append(line)

    return "\n".join(result)


def extract_headings(text: str) -> list[str]:

    headings = []

    for line in text.splitlines():

        heading = classify_heading(line)

        if heading:
            headings.append(line.strip())

    return headings