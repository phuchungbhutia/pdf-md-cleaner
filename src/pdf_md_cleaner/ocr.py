from dataclasses import dataclass
from PIL import Image
import pytesseract
import os

# Default installation paths for Windows
default_tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(default_tesseract_path):
  pytesseract.pytesseract.tesseract_cmd = default_tesseract_path

@dataclass
class OCRResult:
    text: str
    confidence: float
    words: list[dict]


def ocr_image(
    image: Image.Image,
    language: str = "eng",
    psm: int = 3,
) -> OCRResult:

    config = f"--oem 3 --psm {psm}"

    text = pytesseract.image_to_string(
        image,
        lang=language,
        config=config,
    )

    data = pytesseract.image_to_data(
        image,
        lang=language,
        config=config,
        output_type=pytesseract.Output.DICT,
    )

    confidences = []
    words = []

    for index, raw_confidence in enumerate(
        data["conf"]
    ):
        try:
            confidence = float(raw_confidence)
        except (ValueError, TypeError):
            continue

        if confidence >= 0:
            confidences.append(confidence)

            words.append(
                {
                    "text": data["text"][index],
                    "confidence": confidence,
                    "left": data["left"][index],
                    "top": data["top"][index],
                    "width": data["width"][index],
                    "height": data["height"][index],
                }
            )

    average_confidence = (
        sum(confidences) / len(confidences)
        if confidences
        else 0.0
    )

    return OCRResult(
        text=text.strip(),
        confidence=average_confidence,
        words=words,
    )


def check_tesseract() -> bool:
    try:
        version = pytesseract.get_tesseract_version()
        return version is not None
    except Exception:
        return False
