import re
from typing import List, Optional

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

def is_noise_line(line: str) -> bool:
  """Detect lines that are scanner artifacts, border noise, or stray symbols."""
  cleaned = line.strip()
  if not cleaned:
    return True

  # Single stray punctuation/character noise like 'é', 't-', 'q', 'y'
  if len(cleaned) <= 2 and not cleaned.isalnum():
    return True

  # Lines where non-alphanumeric chars dominate (> 50% noise)
  alnum_count = sum(c.isalnum() for c in cleaned)
  if len(cleaned) > 3 and (alnum_count / len(cleaned)) < 0.45:
    return True

  # Repetitive scanning artifacts (e.g., 'ycuvccccce', 'eeeeeee', '.......')
  if re.search(r"(.)\1{4,}", cleaned):
    return True

  # High ratio of standalone single letters: "a ia ile Sn i il a a eS"
  words = cleaned.split()
  if len(words) >= 4:
    single_char_words = [w for w in words if len(w) == 1]
    if len(single_char_words) / len(words) > 0.5:
      return True

  return False


def clean_page_lines(raw_text: str) -> str:
  """Filter out noisy lines and normalize document line flow."""
  lines = raw_text.splitlines()
  good_lines: List[str] = []

  for line in lines:
    stripped = line.strip()
    if is_noise_line(stripped):
      continue

    # Fix common Indian CAG / Audit document OCR confusions
    line_fixed = stripped
    line_fixed = re.sub(
        r"\b(Fart|Fert)\b", "Part", line_fixed, flags=re.IGNORECASE
    )
    line_fixed = re.sub(r"\bLBA\s*\(HQs?\)", "LBA (HQ)", line_fixed)
    line_fixed = re.sub(r"\b(ATIR|AT1R)\b", "ATIR", line_fixed)
    line_fixed = re.sub(r"\b(PRIs?/ULBs?)\b", "PRIs/ULBs", line_fixed)

    good_lines.append(line_fixed)

  return "\n".join(good_lines)


def is_valid_heading(candidate: str) -> bool:
  """Validate if a line legitimately qualifies as a Markdown heading."""
  text = candidate.strip("# ").strip()

  # Disallow headings that are noise or single words with garbled chars
  if len(text) < 3 or is_noise_line(text):
    return False

  # Must have reasonable alphabetic content
  letters = [c for c in text if c.isalpha()]
  if len(letters) < 3:
    return False

  # Headings shouldn't be full multi-line paragraphs accidentally flagged
  if len(text.split()) > 14:
    return False

  return True