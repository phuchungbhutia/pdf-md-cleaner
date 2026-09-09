from pdf_md_cleaner.structure import (
    classify_heading,
    extract_headings,
)


def test_rule_heading():

    assert (
        classify_heading(
            "Rule 12. Conditions"
        )
        == "h2"
    )


def test_numbered_heading():

    assert (
        classify_heading(
            "1. Introduction"
        )
        == "h3"
    )


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
