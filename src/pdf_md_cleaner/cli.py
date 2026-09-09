import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .config import CleanerConfig
from .ocr import is_tesseract_available
from .pipeline import process_pdf, write_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract and clean PDF documents to Markdown."
    )

    parser.add_argument(
        "input_path",
        nargs="?",
        default=None,
        type=Path,
        help=(
            "Path to an input PDF file or a directory containing PDFs. "
            "Defaults to './input' if omitted."
        ),
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help=(
            "Output Markdown file path (for a single PDF) or output directory "
            "(for batch processing). Defaults to './output'."
        ),
    )

    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="Optional path to write JSON extraction report.",
    )

    parser.add_argument(
        "--no-toc",
        action="store_true",
        help="Disable automatic table of contents generation.",
    )

    parser.add_argument(
        "--no-tables",
        action="store_true",
        help="Disable simple table detection.",
    )

    parser.add_argument(
        "--language",
        type=str,
        default="eng",
        help="OCR language (default: eng).",
    )

    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Rendering DPI for OCR fallback (default: 300).",
    )

    return parser


def find_pdf_files(target_dir: Path) -> List[Path]:
    """Find all .pdf files inside a directory (case-insensitive)."""
    return sorted(
        [
            p
            for p in target_dir.iterdir()
            if p.is_file() and p.suffix.lower() == ".pdf"
        ]
    )


def process_single(
    pdf_path: Path,
    out_file: Path,
    config: CleanerConfig,
    report_path: Optional[Path] = None,
) -> None:
    print(f"\nProcessing: {pdf_path.name} -> {out_file}")
    result = process_pdf(pdf_path, out_file, config)

    if report_path:
        write_report(result, report_path)

    print(
        f"Done: {result.total_pages} pages processed "
        f"({result.ocr_pages} via OCR, {result.review_pages} need review)."
    )


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not is_tesseract_available():
        print("WARNING: Tesseract OCR was not detected.")
        print("Native PDFs may still work.")
        print("Install Tesseract for scanned PDFs.")

    config = CleanerConfig(
        language=args.language,
        dpi=args.dpi,
        generate_toc=not args.no_toc,
        detect_tables=not args.no_tables,
    )

    # 1. Resolve input target (default to ./input directory if omitted)
    if args.input_path is None:
        input_target = Path("input")
    else:
        input_target = args.input_path

    # Check existence
    if not input_target.exists():
        print(f"Error: Input path does not exist: {input_target}", file=sys.stderr)
        sys.exit(1)

    # 2. Batch Mode: Directory input
    if input_target.is_dir():
        pdf_files = find_pdf_files(input_target)
        if not pdf_files:
            print(f"No PDF files found in directory: {input_target}")
            sys.exit(0)

        out_dir = args.output if args.output is not None else Path("output")
        out_dir.mkdir(parents=True, exist_ok=True)

        print(f"Found {len(pdf_files)} PDF(s) in '{input_target}'. Converting...")

        for pdf_file in pdf_files:
            out_file = out_dir / f"{pdf_file.stem}.md"
            report_file = (
                args.report
                if len(pdf_files) == 1
                else (out_dir / f"{pdf_file.stem}.report.json")
            )
            process_single(pdf_file, out_file, config, report_file)

        print(f"\nAll conversions complete. Results saved in: {out_dir}")

    # 3. Single File Mode: Specific PDF passed
    elif input_target.is_file():
        if args.output is not None:
            # If user provided a directory path ending with slash or an existing dir
            if args.output.is_dir() or str(args.output).endswith(("/", "\\")):
                out_file = args.output / f"{input_target.stem}.md"
            else:
                out_file = args.output
        else:
            out_file = Path("output") / f"{input_target.stem}.md"

        process_single(input_target, out_file, config, args.report)


if __name__ == "__main__":
    main()
