from pathlib import Path
import pymupdf as fitz
from PIL import Image

def open_pdf(path: Path) -> fitz.Document:
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected PDF file: {path}")

    return fitz.open(path)


def render_page(
    page: fitz.Page,
    dpi: int = 300,
) -> Image.Image:
    """
    Render a PDF page into a PIL image.
    """

    scale = dpi / 72.0

    matrix = fitz.Matrix(scale, scale)

    pixmap = page.get_pixmap(
        matrix=matrix,
        alpha=False,
    )

    return Image.frombytes(
        "RGB",
        [pixmap.width, pixmap.height],
        pixmap.samples,
    )


def extract_native_text(page: fitz.Page) -> str:
    """
    Extract embedded text from a PDF page.
    """

    return page.get_text("text").strip()


def page_has_images(page: fitz.Page) -> bool:
    return len(page.get_images(full=True)) > 0


def pdf_page_count(document: fitz.Document) -> int:
    return len(document)
