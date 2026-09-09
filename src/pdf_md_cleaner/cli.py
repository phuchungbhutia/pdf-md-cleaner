import argparse
from pathlib import Path

from .config import CleanerConfig
from .ocr import check_tesseract
from .pipeline import process_pdf, write_report


def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        prog="pdf-md-cleaner",
        description=(
            "Convert native and scanned PDFs "
            "into structured Markdown."
        ),
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input PDF file.",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        help="Output Markdown file.",
    )

    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="OCR rendering DPI. Default: 300.",
    )

    parser.add_argument(
        "--lang",
        default="eng",
        help="Tesseract language. Default: eng.",
    )

    parser.add_argument(
        "--psm",
        type=int,
        default=3,
        help="Tesseract page segmentation mode.",
    )

    parser.add_argument(
        "--min-confidence",
        type=float,
        default=70.0,
        help="Minimum OCR confidence before review is required.",
    )

    parser.add_argument(
        "--report",
        type=Path,
        help="Optional JSON quality-control report.",
    )

    parser.add_argument(
        "--no-toc",
        action="store_true",
        help="Disable automatic TOC generation.",
    )

    parser.add_argument(
        "--no-page-markers",
        action="store_true",
        help="Disable source page comments.",
    )

    parser.add_argument(
        "--no-tables",
        action="store_true",
        help="Disable simple table detection.",
    )

    return parser


def main() -> None:

    parser = build_parser()

    args = parser.parse_args()

    input_file = args.input

    if not input_file.exists():

        parser.error(
            f"Input file does not exist: "
            f"{input_file}"
        )

    if not check_tesseract():

        print(
            "WARNING: Tesseract OCR was not detected."
        )

        print(
            "Native PDFs may still work."
        )

        print(
            "Install Tesseract for scanned PDFs."
        )

    config = CleanerConfig(
        dpi=args.dpi,
        language=args.lang,
        ocr_psm=args.psm,
        min_ocr_confidence=args.min_confidence,
        generate_toc=not args.no_toc,
        preserve_page_markers=not args.no_page_markers,
        detect_tables=not args.no_tables,
    )

    result = process_pdf(
        input_file,
        args.output,
        config,
    )

    report_file = args.report

    if report_file is None:

        report_file = (
            args.output.with_suffix(
                ".report.json"
            )
        )

    write_report(
        result,
        report_file,
    )

    print()
    print("Processing complete.")
    print(
        f"Pages: {result.total_pages}"
    )
    print(
        f"OCR pages: {result.ocr_pages}"
    )
    print(
        f"Review pages: {result.review_pages}"
    )
    print(
        f"Markdown: {args.output}"
    )
    print(
        f"Report: {report_file}"
    )


if __name__ == "__main__":
    main()
