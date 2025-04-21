from cleaner.markdown_cleaner import clean_markdown

def test_cleaning():
    dirty_text = "Page 1\nTHIS IS A HEADING\nSome text\nMore text"
    patterns = [r'^Page\s+\d+\s*$']
    cleaned = clean_markdown(dirty_text, patterns)
    assert "Page" not in cleaned
    assert "## This Is A Heading" in cleaned
