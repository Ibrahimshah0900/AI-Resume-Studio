
from __future__ import annotations

import re
from collections import OrderedDict
from typing import Dict, List, Tuple

from utils.text_cleaner import clean_resume_text


SECTION_ALIASES = {
    "summary": {"summary", "professional summary", "profile", "professional profile", "career summary", "objective"},
    "experience": {"experience", "work experience", "professional experience", "employment history", "work history"},
    "education": {"education", "educational background", "academic background", "qualifications"},
    "skills": {"skills", "technical skills", "core skills", "key skills", "professional skills", "technical expertise"},
    "projects": {"projects", "personal projects", "academic projects", "key projects", "selected projects"},
    "certifications": {"certifications", "certificates", "licenses & certifications", "professional certifications"},
    "languages": {"languages", "language skills", "spoken languages"},
    "achievements": {"achievements", "key achievements", "professional achievements", "accomplishments"},
    "awards": {"awards", "honors", "honours", "awards & honors"},
}

ALIAS_TO_SECTION = {
    alias: section
    for section, aliases in SECTION_ALIASES.items()
    for alias in aliases
}


def normalize_heading(heading: str) -> str:
    heading = heading.strip().lower()
    heading = re.sub(r"[:\-–—]+$", "", heading)
    heading = re.sub(r"\s*&\s*", " & ", heading)
    heading = re.sub(r"\s+", " ", heading)
    return heading.strip()


def detect_heading(line: str) -> str | None:
    normalized = normalize_heading(line)
    if not normalized:
        return None
    if normalized in ALIAS_TO_SECTION:
        return ALIAS_TO_SECTION[normalized]
    numbered = re.sub(r"^\s*\d+\s*[\.\)]\s*", "", normalized)
    if numbered in ALIAS_TO_SECTION:
        return ALIAS_TO_SECTION[numbered]
    return None


def detect_sections(text: str) -> Dict[str, str]:
    cleaned = clean_resume_text(text)
    if not cleaned:
        return OrderedDict()

    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    if not lines:
        return OrderedDict()

    sections = OrderedDict()
    current_section = None
    current_content = []

    def save_current_section():
        nonlocal current_section, current_content
        if current_section is None:
            return
        content = "\n".join(current_content).strip()
        if content:
            if current_section in sections:
                sections[current_section] += "\n" + content
            else:
                sections[current_section] = content
        current_content = []

    for line in lines:
        detected = detect_heading(line)
        if detected is not None:
            save_current_section()
            current_section = detected
            continue
        if current_section is None:
            current_section = "personal_information"
        current_content.append(line)

    save_current_section()
    return sections


def detect_section_names(text: str) -> List[str]:
    return list(detect_sections(text).keys())


def get_section_text(text: str, section: str) -> str:
    return detect_sections(text).get(section, "")
