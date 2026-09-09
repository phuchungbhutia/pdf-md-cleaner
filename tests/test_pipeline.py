from pathlib import Path

import pytest

from pdf_md_cleaner.config import CleanerConfig
from pdf_md_cleaner.pipeline import process_pdf


def test_missing_pdf():
    missing = Path("this-file-does-not-exist.pdf")

    with pytest.raises(FileNotFoundError):
        process_pdf(
            missing,
            Path("output/test.md"),
            CleanerConfig(),
        )
