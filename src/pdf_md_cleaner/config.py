from dataclasses import dataclass


@dataclass
class CleanerConfig:
    dpi: int = 300

    language: str = "eng"

    ocr_psm: int = 3

    min_native_chars: int = 40

    min_ocr_confidence: float = 70.0

    remove_headers: bool = True

    remove_footers: bool = True

    detect_tables: bool = True

    generate_toc: bool = True

    preserve_page_markers: bool = True

    review_marker: str = "REVIEW REQUIRED"

    output_encoding: str = "utf-8"
