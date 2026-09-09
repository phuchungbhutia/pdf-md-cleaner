from PIL import Image

import cv2
import numpy as np


def pil_to_cv(image: Image.Image) -> np.ndarray:
    return cv2.cvtColor(
        np.array(image),
        cv2.COLOR_RGB2BGR,
    )


def cv_to_pil(image: np.ndarray) -> Image.Image:
    return Image.fromarray(
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    )


def grayscale(image: Image.Image) -> Image.Image:
    cv_image = pil_to_cv(image)

    gray = cv2.cvtColor(
        cv_image,
        cv2.COLOR_BGR2GRAY,
    )

    return Image.fromarray(gray)


def denoise(image: Image.Image) -> Image.Image:
    gray = np.array(
        grayscale(image)
    )

    cleaned = cv2.medianBlur(
        gray,
        3,
    )

    return Image.fromarray(cleaned)


def adaptive_threshold(
    image: Image.Image,
) -> Image.Image:

    gray = np.array(
        grayscale(image)
    )

    processed = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15,
    )

    return Image.fromarray(processed)


def sharpen(image: Image.Image) -> Image.Image:
    cv_image = np.array(
        grayscale(image)
    )

    kernel = np.array(
        [
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0],
        ]
    )

    result = cv2.filter2D(
        cv_image,
        -1,
        kernel,
    )

    return Image.fromarray(result)


def preprocess_for_ocr(
    image: Image.Image,
) -> Image.Image:
    """
    General OCR preprocessing pipeline.
    """

    image = denoise(image)

    image = adaptive_threshold(image)

    image = sharpen(image)

    return image
