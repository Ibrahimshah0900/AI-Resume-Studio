
from __future__ import annotations

import re
import unicodedata


def normalize_unicode(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string.")
    return unicodedata.normalize("NFKC", text)


def normalize_line_endings(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def normalize_whitespace(text: str) -> str:
    lines = []
    for line in text.split("\n"):
        line = line.replace("\t", " ")
        line = re.sub(r"[ ]{2,}", " ", line)
        lines.append(line.strip())
    return "\n".join(lines)


def remove_control_characters(text: str) -> str:
    return "".join(
        char for char in text
        if (char in "\n\t" or not unicodedata.category(char).startswith("C"))
    )


def collapse_blank_lines(text: str, max_consecutive: int = 2) -> str:
    if max_consecutive < 1:
        raise ValueError("max_consecutive must be >= 1.")
    pattern = r"\n{" + str(max_consecutive + 1) + r",}"
    replacement = "\n" * max_consecutive
    return re.sub(pattern, replacement, text)


def clean_ocr_artifacts(text: str) -> str:
    replacements = {"\u00a0": " ", "\u200b": "", "\ufeff": ""}
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    return text


def clean_resume_text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string.")
    if not text.strip():
        return ""
    text = normalize_unicode(text)
    text = normalize_line_endings(text)
    text = remove_control_characters(text)
    text = clean_ocr_artifacts(text)
    text = normalize_whitespace(text)
    text = collapse_blank_lines(text)
    return text.strip()


def clean_for_matching(text: str) -> str:
    text = clean_resume_text(text)
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()
