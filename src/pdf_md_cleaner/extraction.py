from pathlib import Path
from typing import List, Union
import pymupdf as fitz
from .cleanup import clean_ocr_text
from .config import CleanerConfig
from .models import PageResult
from .ocr import ocr_image
from .pdf import extract_native_text, render_page
from .preprocessing import preprocess_for_ocr
from .tables import detect_simple_tables


def extract_page(
    page: fitz.Page,
    page_number: int,
    config: CleanerConfig,
) -> PageResult:
    native_text = extract_native_text(page)

    # Native PDF text is preferred when enough text exists.
    if len(native_text.strip()) >= config.min_native_chars:
        cleaned = clean_ocr_text(native_text)
        tables = []

        if config.detect_tables:
            tables = detect_simple_tables(
                cleaned,
                page_number,
            )

        return PageResult(
            page_number=page_number,
            text=cleaned,
            source_type="native",
            ocr_used=False,
            tables=tables,
        )

    # Otherwise use OCR.
    image = render_page(
        page,
        dpi=config.dpi,
    )

    processed = preprocess_for_ocr(image)

    ocr_result = ocr_image(
        processed,
        language=config.language,
        psm=config.ocr_psm,
    )

    cleaned = clean_ocr_text(ocr_result.text)

    review_required = ocr_result.confidence < config.min_ocr_confidence

    warnings = []
    if review_required:
        warnings.append(
            f"OCR confidence is low: {ocr_result.confidence:.1f}%"
        )

    tables = []
    if config.detect_tables:
        tables = detect_simple_tables(
            cleaned,
            page_number,
        )

    return PageResult(
        page_number=page_number,
        text=cleaned,
        source_type="ocr",
        ocr_used=True,
        ocr_confidence=ocr_result.confidence,
        review_required=review_required,
        warnings=warnings,
        tables=tables,
    )


def extract_document(
    input_file: Union[Path, str],
    config: CleanerConfig,
) -> List[PageResult]:
    input_path = Path(input_file)
    if not input_path.is_file():
        raise FileNotFoundError(f"PDF file not found: {input_path}")

    document = fitz.open(input_path)
    pages: List[PageResult] = []

    try:
        total_pages = len(document)
        for number, page in enumerate(document, start=1):
            print(f"Processing page {number}/{total_pages}...")
            result = extract_page(
                page,
                number,
                config,
            )
            pages.append(result)
    finally:
        document.close()

    return pages
