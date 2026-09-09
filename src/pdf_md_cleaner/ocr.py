import os
import shutil
from dataclasses import dataclass

from PIL import Image
import pytesseract


@dataclass
class OCRResult:
    text: str
    confidence: float


# Auto-configure Tesseract binary path on Windows if not in PATH
if os.name == "nt":
    common_windows_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.expanduser(r"~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"),
    ]
    for path in common_windows_paths:
        if os.path.isfile(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break


def is_tesseract_available() -> bool:
    """Check if the Tesseract binary is discoverable and callable."""
    # Check if custom configured path exists
    if os.path.isfile(pytesseract.pytesseract.tesseract_cmd):
        return True

    # Check if 'tesseract' is available in system PATH
    if shutil.which("tesseract") is not None:
        return True

    # Try checking version directly via pytesseract
    try:
        version = pytesseract.get_tesseract_version()
        return version is not None
    except Exception:
        return False


def ocr_image(
    image: Image.Image,
    language: str = "eng",
    psm: int = 3,
) -> OCRResult:
    """Run OCR on a PIL Image and calculate mean word-level confidence."""
    custom_config = f"--oem 3 --psm {psm}"

    # Extract text
    text = pytesseract.image_to_string(
        image,
        lang=language,
        config=custom_config,
    )

    # Extract word confidence scores
    confidences = []
    try:
        data = pytesseract.image_to_data(
            image,
            lang=language,
            config=custom_config,
            output_type=pytesseract.Output.DICT,
        )
        for conf in data.get("conf", []):
            try:
                score = float(conf)
                if score >= 0:
                    confidences.append(score)
            except (ValueError, TypeError):
                continue
    except Exception:
        pass

    average_confidence = (
        sum(confidences) / len(confidences) if confidences else 0.0
    )

    return OCRResult(
        text=text,
        confidence=average_confidence,
    )
