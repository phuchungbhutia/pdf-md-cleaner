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


def preprocess_for_ocr(pil_image: Image.Image) -> Image.Image:
  """Denoise, deskew, and threshold image to prevent margin OCR artifacts."""
  img = np.array(pil_image)

  # Convert to grayscale
  if len(img.shape) == 3:
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
  else:
    gray = img

  # 1. Remove black borders / margin noise from scanning bed
  h, w = gray.shape
  margin_h = int(h * 0.02)
  margin_w = int(w * 0.02)
  # Mask outermost 2% borders to white
  gray[:margin_h, :] = 255
  gray[-margin_h:, :] = 255
  gray[:, :margin_w] = 255
  gray[:, -margin_w:] = 255

  # 2. Otsu Binarization (converts gray smudge to clean black & white)
  _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

  # 3. Median blur to remove salt-and-pepper dust
  denoised = cv2.medianBlur(thresh, 3)

  return Image.fromarray(denoised)
