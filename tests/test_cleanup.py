from pdf_md_cleaner.cleanup import (
    clean_ocr_text,
    repair_line_breaks,
)


def test_repair_hyphenated_word():

    text = "govern-\nment"

    result = repair_line_breaks(text)

    assert result == "government"


def test_remove_page_number():

    text = "Some text\n25\nMore text"

    result = clean_ocr_text(text)

    assert "25" not in result


def test_normalize_whitespace():

    text = "Hello     world"

    result = clean_ocr_text(text)

    assert result == "Hello world"