from pdf_md_cleaner.markdown import (
    table_to_markdown,
)


def test_table_conversion():

    rows = [
        ["Name", "Value"],
        ["Test", "100"],
    ]

    result = table_to_markdown(rows)

    assert "| Name | Value |" in result
    assert "| --- | --- |" in result
    assert "| Test | 100 |" in result


def test_pipe_is_escaped():

    rows = [
        ["A|B", "Value"],
        ["Test", "1"],
    ]

    result = table_to_markdown(rows)

    assert r"A\|B" in result