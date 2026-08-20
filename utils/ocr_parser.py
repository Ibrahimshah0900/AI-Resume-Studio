
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
import pytesseract
from PIL import Image


SUPPORTED_IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
}


@dataclass
class OCRResult:
    text: str
    character_count: int
    success: bool
    confidence: Optional[float] = None
    error: Optional[str] = None

    @property
    def has_text(self) -> bool:
        return bool(self.text.strip())


def load_image(file_path: str | Path) -> np.ndarray:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Image does not exist: {path}")
    image = cv2.imread(str(path))
    if image is None:
        raise ValueError(f"Unable to decode image: {path}")
    return image


def preprocess_image(image: np.ndarray) -> np.ndarray:
    if image is None or image.size == 0:
        raise ValueError("The supplied image is empty.")
    if len(image.shape) == 3:
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        grayscale = image.copy()
    denoised = cv2.GaussianBlur(grayscale, (3, 3), 0)
    thresholded = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11,
    )
    return thresholded


def _calculate_average_confidence(image: np.ndarray) -> Optional[float]:
    try:
        data = pytesseract.image_to_data(
            image,
            output_type=pytesseract.Output.DICT,
        )
        confidences = []
        for value in data.get("conf", []):
            try:
                confidence = float(value)
                if confidence >= 0:
                    confidences.append(confidence)
            except (TypeError, ValueError):
                continue
        if not confidences:
            return None
        return round(float(np.mean(confidences)), 2)
    except Exception:
        return None


def extract_image_text(file_path: str | Path) -> OCRResult:
    path = Path(file_path)

    if not path.exists():
        return OCRResult(
            text="",
            character_count=0,
            success=False,
            error=f"File does not exist: {path}",
        )

    if path.suffix.lower() not in SUPPORTED_IMAGE_EXTENSIONS:
        return OCRResult(
            text="",
            character_count=0,
            success=False,
            error="Unsupported image format. Use PNG, JPG, or JPEG.",
        )

    try:
        image = load_image(path)
        processed_image = preprocess_image(image)
        text = pytesseract.image_to_string(
            processed_image,
            config="--psm 6",
        ).strip()
        confidence = _calculate_average_confidence(processed_image)

        return OCRResult(
            text=text,
            character_count=len(text),
            success=True,
            confidence=confidence,
        )

    except Exception as exc:
        return OCRResult(
            text="",
            character_count=0,
            success=False,
            error=f"OCR failed: {exc}",
        )
