import unittest
from cleaner.markdown_cleaner import clean_markdown_file

class TestMarkdownCleaner(unittest.TestCase):
    def test_remove_page_numbers(self):
        input_text = "Page 1\n# Heading 1\nContent here."
        expected_output = "# Heading 1\nContent here."
        cleaned_text = clean_markdown_file(input_text)
        self.assertIn("# Heading 1", cleaned_text)
        self.assertNotIn("Page 1", cleaned_text)

    def test_fix_spacing(self):
        input_text = "#Heading1\nContent here."
        expected_output = "# Heading 1\nContent here."
        cleaned_text = clean_markdown_file(input_text)
        self.assertIn("Heading", cleaned_text)

    def test_preserve_structure(self):
        input_text = "# Title\n\n## Subtitle\n\nSome text here."
        cleaned_text = clean_markdown_file(input_text)
        self.assertIn("# Title", cleaned_text)
        self.assertIn("## Subtitle", cleaned_text)

if __name__ == "__main__":
    unittest.main()
