from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TextBlock:
    text: str
    x0: float = 0.0
    y0: float = 0.0
    x1: float = 0.0
    y1: float = 0.0
    confidence: Optional[float] = None
    block_type: str = "text"
    page_number: int = 1


@dataclass
class TableData:
    rows: list[list[str]] = field(default_factory=list)
    page_number: int = 1


@dataclass
class PageResult:
    page_number: int
    text: str = ""
    blocks: list[TextBlock] = field(default_factory=list)
    tables: list[TableData] = field(default_factory=list)

    source_type: str = "native"

    ocr_used: bool = False
    ocr_confidence: Optional[float] = None

    review_required: bool = False
    warnings: list[str] = field(default_factory=list)


@dataclass
class DocumentResult:
    source_file: str
    output_file: str

    pages: list[PageResult] = field(default_factory=list)

    title: str = "Transcribed Document"

    total_pages: int = 0
    ocr_pages: int = 0
    review_pages: int = 0

    warnings: list[str] = field(default_factory=list)
