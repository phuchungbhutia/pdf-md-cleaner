import re


OCR_REPLACEMENTS = {
    "\u00a0": " ",
    "ﬁ": "fi",
    "ﬂ": "fl",
    "ﬀ": "ff",
    "ﬃ": "ffi",
    "ﬄ": "ffl",
}


def normalize_unicode(text: str) -> str:

    for old, new in OCR_REPLACEMENTS.items():
        text = text.replace(old, new)

    return text


def normalize_whitespace(text: str) -> str:

    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()


def repair_line_breaks(text: str) -> str:
    """
    Join words broken across lines.

    Example:

        govern-
        ment

    becomes:

        government
    """

    text = re.sub(
        r"(\w)-\n(\w)",
        r"\1\2",
        text,
    )

    return text


def remove_running_page_numbers(
    text: str,
) -> str:

    lines = text.splitlines()

    cleaned = []

    for line in lines:

        stripped = line.strip()

        if re.fullmatch(
            r"(page\s*)?\d+",
            stripped,
            flags=re.IGNORECASE,
        ):
            continue

        cleaned.append(line)

    return "\n".join(cleaned)


def clean_ocr_text(
    text: str,
) -> str:

    text = normalize_unicode(text)

    text = repair_line_breaks(text)

    text = remove_running_page_numbers(text)

    text = normalize_whitespace(text)

    return text
