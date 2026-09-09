from pdf_md_cleaner.structure import (
    extract_headings,
    is_numbered_heading,
    is_rule_heading,
)


def test_rule_heading():
    assert is_rule_heading("Rule 1. General")
    assert is_rule_heading("Rule 2: Scope of Work")
    assert not is_rule_heading("This is just regular text mentioning Rule 1.")


def test_numbered_heading():
    assert is_numbered_heading("1.1 Definitions")
    assert is_numbered_heading("2.3.1 Scope of Inspection")
    assert not is_numbered_heading("There are 1.1 million items remaining.")


def test_extract_headings():
    text = """
    Rule 1. General
    This is normal text.

    1.1 Definitions
    More text.
    """

    headings = extract_headings(text)

    assert "Rule 1. General" in headings
    assert "1.1 Definitions" in headings
