
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import cv2
import numpy as np


@dataclass
class CVAnalysisResult:
    success: bool
    width: int = 0
    height: int = 0
    resolution_label: str = "unknown"
    blur_score: float = 0.0
    blur_label: str = "unknown"
    brightness: float = 0.0
    contrast: float = 0.0
    orientation: str = "unknown"
    whitespace_ratio: float = 0.0
    content_ratio: float = 0.0
    layout_type: str = "unknown"
    warnings: list[str] | None = None
    suggestions: list[str] | None = None
    error: str | None = None


def load_image(image_path: str | Path) -> np.ndarray:
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image does not exist: {path}")
    image = cv2.imread(str(path))
    if image is None:
        raise ValueError(f"Unable to decode image: {path}")
    return image


def calculate_blur_score(image: np.ndarray) -> float:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def classify_blur(blur_score: float) -> str:
    if blur_score < 50:
        return "very_blurry"
    if blur_score < 120:
        return "blurry"
    if blur_score < 300:
        return "acceptable"
    return "sharp"


def calculate_brightness(image: np.ndarray) -> float:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return float(np.mean(gray))


def calculate_contrast(image: np.ndarray) -> float:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return float(np.std(gray))


def classify_resolution(width: int, height: int) -> str:
    pixels = width * height
    if min(width, height) < 500 or pixels < 300_000:
        return "low"
    if min(width, height) < 900 or pixels < 1_000_000:
        return "acceptable"
    return "good"


def detect_orientation(image: np.ndarray) -> str:
    height, width = image.shape[:2]
    if height > width * 1.15:
        return "portrait"
    if width > height * 1.15:
        return "landscape"
    return "square_or_unclear"


def estimate_whitespace(image: np.ndarray) -> tuple[float, float]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    binary = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15,
    )
    content_pixels = np.sum(binary == 0)
    total_pixels = binary.size
    content_ratio = float(content_pixels / total_pixels)
    whitespace_ratio = float(1.0 - content_ratio)
    return whitespace_ratio, content_ratio


def detect_layout(image: np.ndarray) -> str:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15,
    )
    content = (binary == 0).astype(np.uint8)
    column_projection = np.sum(content, axis=0)
    if column_projection.size == 0:
        return "unknown"
    threshold = max(1, int(np.max(column_projection) * 0.08))
    active_columns = column_projection > threshold
    transitions = np.diff(active_columns.astype(np.int8))
    starts = int(np.sum(transitions == 1))
    if starts >= 2:
        return "possible_multi_column"
    return "single_column_or_simple_layout"


def generate_quality_feedback(
    resolution_label: str,
    blur_label: str,
    brightness: float,
    contrast: float,
    orientation: str,
    whitespace_ratio: float,
    content_ratio: float,
) -> tuple[list[str], list[str]]:
    warnings = []
    suggestions = []

    if resolution_label == "low":
        warnings.append("Page appears low resolution.")
        suggestions.append("Upload a higher-resolution PDF or image when possible.")

    if blur_label in {"very_blurry", "blurry"}:
        warnings.append("Page may be blurry or difficult to read.")
        suggestions.append("Use a sharper scan or export the resume at higher quality.")

    if brightness < 55:
        warnings.append("Page appears unusually dark.")
        suggestions.append("Improve lighting or document brightness before uploading.")
    elif brightness > 245:
        warnings.append("Page appears unusually bright.")
        suggestions.append("Check whether text is being lost because of overexposure.")

    if contrast < 20:
        warnings.append("Low contrast detected.")
        suggestions.append("Use darker text and a clearer background.")

    if orientation == "landscape":
        warnings.append("Landscape orientation detected.")
        suggestions.append("Check whether portrait orientation would be more appropriate.")
    elif orientation == "portrait":
        suggestions.append("Portrait orientation looks appropriate for a resume.")

    if whitespace_ratio > 0.70:
        warnings.append("Large amount of whitespace detected.")
        suggestions.append("Consider improving content balance if important information is missing.")

    if content_ratio > 0.45:
        warnings.append("Page appears visually dense.")
        suggestions.append("Consider improving spacing and reducing unnecessary text.")

    if not warnings:
        suggestions.append("No major visual-quality warnings detected.")

    return warnings, suggestions


def analyze_resume_image(image_path: str | Path) -> CVAnalysisResult:
    try:
        image = load_image(image_path)
        height, width = image.shape[:2]

        resolution_label = classify_resolution(width, height)
        blur_score = calculate_blur_score(image)
        blur_label = classify_blur(blur_score)
        brightness = calculate_brightness(image)
        contrast = calculate_contrast(image)
        orientation = detect_orientation(image)
        whitespace_ratio, content_ratio = estimate_whitespace(image)
        layout_type = detect_layout(image)

        warnings, suggestions = generate_quality_feedback(
            resolution_label=resolution_label,
            blur_label=blur_label,
            brightness=brightness,
            contrast=contrast,
            orientation=orientation,
            whitespace_ratio=whitespace_ratio,
            content_ratio=content_ratio,
        )

        return CVAnalysisResult(
            success=True,
            width=width,
            height=height,
            resolution_label=resolution_label,
            blur_score=round(blur_score, 2),
            blur_label=blur_label,
            brightness=round(brightness, 2),
            contrast=round(contrast, 2),
            orientation=orientation,
            whitespace_ratio=round(whitespace_ratio, 4),
            content_ratio=round(content_ratio, 4),
            layout_type=layout_type,
            warnings=warnings,
            suggestions=suggestions,
        )

    except Exception as exc:
        return CVAnalysisResult(
            success=False,
            warnings=[],
            suggestions=[],
            error=str(exc),
        )
