from pathlib import Path

from pdf_md_cleaner.config import CleanerConfig
from pdf_md_cleaner.pipeline import process_pdf


def test_missing_pdf():

    missing = Path(
        "this-file-does-not-exist.pdf"
    )

    try:
        process_pdf(
            missing,
            Path("output/test.md"),
            CleanerConfig(),
        )

        assert False

    except FileNotFoundError:
        assert True