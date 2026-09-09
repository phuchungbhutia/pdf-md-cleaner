import json
from pathlib import Path

from .config import CleanerConfig
from .extraction import extract_document
from .markdown import document_to_markdown
from .models import DocumentResult


def create_document_result(
    input_file: Path,
    output_file: Path,
    config: CleanerConfig,
) -> DocumentResult:
    input_path = Path(input_file)
    if not input_path.is_file():
        raise FileNotFoundError(f"Input file does not exist: {input_path}")

    pages = extract_document(
        input_path,
        config,
    )

    result = DocumentResult(
        source_file=str(input_path.resolve()),
        output_file=str(output_file.resolve()),
        pages=pages,
        total_pages=len(pages),
        ocr_pages=sum(1 for page in pages if page.ocr_used),
        review_pages=sum(1 for page in pages if page.review_required),
    )

    for page in pages:
        result.warnings.extend(page.warnings)

    return result


def process_pdf(
    input_file: Path,
    output_file: Path,
    config: CleanerConfig,
) -> DocumentResult:
    input_path = Path(input_file)
    if not input_path.is_file():
        raise FileNotFoundError(f"Input file does not exist: {input_path}")

    result = create_document_result(
        input_path,
        output_file,
        config,
    )

    markdown = document_to_markdown(
        result,
        generate_toc_enabled=config.generate_toc,
        preserve_page_markers=config.preserve_page_markers,
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file.write_text(
        markdown,
        encoding=config.output_encoding,
    )

    return result


def write_report(
    result: DocumentResult,
    report_file: Path,
) -> None:
    report = {
        "source_file": result.source_file,
        "output_file": result.output_file,
        "total_pages": result.total_pages,
        "ocr_pages": result.ocr_pages,
        "review_pages": result.review_pages,
        "warnings": result.warnings,
        "pages": [
            {
                "page_number": page.page_number,
                "source_type": page.source_type,
                "ocr_used": page.ocr_used,
                "ocr_confidence": page.ocr_confidence,
                "review_required": page.review_required,
                "warnings": page.warnings,
            }
            for page in result.pages
        ],
    }

    report_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_file.write_text(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
