
from __future__ import annotations

from typing import Optional

from utils.data_models import (
    Achievement,
    Certification,
    Education,
    Language,
    PersonalInfo,
    Project,
    Resume,
    WorkExperience,
)


def create_new_resume() -> Resume:
    """Create a completely empty resume."""

    return Resume()


def update_personal_info(
    resume: Resume,
    personal_info: PersonalInfo,
) -> Resume:
    """Replace the resume's personal information."""

    resume.personal_info = personal_info
    return resume


def update_summary(
    resume: Resume,
    summary: str,
) -> Resume:
    """Update the professional summary."""

    resume.summary = summary.strip()
    return resume


def add_experience(
    resume: Resume,
    experience: WorkExperience,
) -> Resume:
    """Add a work experience entry."""

    resume.experience.append(experience)
    return resume


def remove_experience(
    resume: Resume,
    index: int,
) -> Resume:
    """Remove a work experience entry by index."""

    if not 0 <= index < len(resume.experience):
        raise IndexError("Experience index is out of range.")

    resume.experience.pop(index)
    return resume


def move_experience_up(resume: Resume, index: int) -> Resume:
    """Move an experience entry up in the list."""
    if index > 0:
        resume.experience[index], resume.experience[index - 1] = resume.experience[index - 1], resume.experience[index]
    return resume

def move_experience_down(resume: Resume, index: int) -> Resume:
    """Move an experience entry down in the list."""
    if index < len(resume.experience) - 1:
        resume.experience[index], resume.experience[index + 1] = resume.experience[index + 1], resume.experience[index]
    return resume


def add_education(
    resume: Resume,
    education: Education,
) -> Resume:
    """Add an education entry."""

    resume.education.append(education)
    return resume


def remove_education(
    resume: Resume,
    index: int,
) -> Resume:
    """Remove an education entry by index."""

    if not 0 <= index < len(resume.education):
        raise IndexError("Education index is out of range.")

    resume.education.pop(index)
    return resume


def add_skill(
    resume: Resume,
    skill: str,
) -> Resume:
    """Add a skill if it is not already present."""

    normalized_skill = skill.strip()

    if not normalized_skill:
        return resume

    existing = {
        item.strip().lower()
        for item in resume.skills
    }

    if normalized_skill.lower() not in existing:
        resume.skills.append(normalized_skill)

    return resume


def remove_skill(
    resume: Resume,
    skill: str,
) -> Resume:
    """Remove a skill using case-insensitive matching."""

    normalized_skill = skill.strip().lower()

    resume.skills = [
        item
        for item in resume.skills
        if item.strip().lower() != normalized_skill
    ]

    return resume


def add_project(
    resume: Resume,
    project: Project,
) -> Resume:
    """Add a project."""

    resume.projects.append(project)
    return resume


def remove_project(
    resume: Resume,
    index: int,
) -> Resume:
    """Remove a project by index."""

    if not 0 <= index < len(resume.projects):
        raise IndexError("Project index is out of range.")

    resume.projects.pop(index)
    return resume

def move_project_up(resume: Resume, index: int) -> Resume:
    """Move a project entry up in the list."""
    if index > 0:
        resume.projects[index], resume.projects[index - 1] = resume.projects[index - 1], resume.projects[index]
    return resume

def move_project_down(resume: Resume, index: int) -> Resume:
    """Move a project entry down in the list."""
    if index < len(resume.projects) - 1:
        resume.projects[index], resume.projects[index + 1] = resume.projects[index + 1], resume.projects[index]
    return resume


def add_certification(
    resume: Resume,
    certification: Certification,
) -> Resume:
    """Add a certification."""

    resume.certifications.append(certification)
    return resume


def remove_certification(
    resume: Resume,
    index: int,
) -> Resume:
    """Remove a certification by index."""

    if not 0 <= index < len(resume.certifications):
        raise IndexError("Certification index is out of range.")

    resume.certifications.pop(index)
    return resume


def add_language(
    resume: Resume,
    language: Language,
) -> Resume:
    """Add a language."""

    resume.languages.append(language)
    return resume


def remove_language(
    resume: Resume,
    index: int,
) -> Resume:
    """Remove a language by index."""

    if not 0 <= index < len(resume.languages):
        raise IndexError("Language index is out of range.")

    resume.languages.pop(index)
    return resume


def add_achievement(
    resume: Resume,
    achievement: Achievement,
) -> Resume:
    """Add an achievement."""

    resume.achievements.append(achievement)
    return resume


def remove_achievement(
    resume: Resume,
    index: int,
) -> Resume:
    """Remove an achievement by index."""

    if not 0 <= index < len(resume.achievements):
        raise IndexError("Achievement index is out of range.")

    resume.achievements.pop(index)
    return resume


def update_custom_section(
    resume: Resume,
    section_name: str,
    content: str,
) -> Resume:
    """Create or update a custom resume section."""

    name = section_name.strip()

    if not name:
        raise ValueError("Custom section name cannot be empty.")

    content = content.strip()

    if content:
        resume.custom_sections[name] = content
    else:
        resume.custom_sections.pop(name, None)

    return resume


def get_resume_counts(resume: Resume) -> dict[str, int]:
    """Return useful counts for dashboard statistics."""

    return {
        "experience": len(resume.experience),
        "education": len(resume.education),
        "skills": len(resume.skills),
        "projects": len(resume.projects),
        "certifications": len(resume.certifications),
        "languages": len(resume.languages),
        "achievements": len(resume.achievements),
        "custom_sections": len(resume.custom_sections),
    }
