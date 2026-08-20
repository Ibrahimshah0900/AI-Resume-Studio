
from __future__ import annotations

from typing import Dict, List, Tuple

from utils.data_models import Resume


# Weight assigned to each major resume section.
COMPLETION_WEIGHTS: Dict[str, int] = {
    "personal_information": 10,
    "summary": 10,
    "experience": 20,
    "education": 15,
    "skills": 15,
    "projects": 15,
    "certifications": 5,
    "languages": 5,
    "achievements": 5,
}


def _has_personal_information(resume: Resume) -> bool:
    """Check whether meaningful personal information exists."""

    info = resume.personal_info

    meaningful_fields = [
        info.full_name.strip(),
        info.professional_title.strip(),
        str(info.email) if info.email else "",
        info.phone.strip(),
        info.location.strip(),
    ]

    return bool(
        info.full_name.strip()
        and any(field.strip() for field in meaningful_fields[1:])
    )


def _has_summary(resume: Resume) -> bool:
    """Check whether the professional summary contains useful content."""

    return len(resume.summary.strip()) >= 40


def _has_experience(resume: Resume) -> bool:
    """Check whether meaningful work experience exists."""

    for item in resume.experience:
        if (
            item.job_title.strip()
            and item.company.strip()
            and (
                item.description.strip()
                or len(item.bullet_points) > 0
            )
        ):
            return True

    return False


def _has_education(resume: Resume) -> bool:
    """Check whether meaningful education information exists."""

    for item in resume.education:
        if item.institution.strip() and (
            item.degree.strip() or item.field_of_study.strip()
        ):
            return True

    return False


def _has_skills(resume: Resume) -> bool:
    """Check whether at least three meaningful skills exist."""

    valid_skills = {
        skill.strip().lower()
        for skill in resume.skills
        if skill.strip()
    }

    return len(valid_skills) >= 3


def _has_projects(resume: Resume) -> bool:
    """Check whether at least one meaningful project exists."""

    for item in resume.projects:
        if item.name.strip() and (
            item.description.strip()
            or len(item.technologies) > 0
            or len(item.bullet_points) > 0
        ):
            return True

    return False


def _has_certifications(resume: Resume) -> bool:
    """Check whether at least one meaningful certification exists."""

    for item in resume.certifications:
        if item.name.strip() and item.issuing_organization.strip():
            return True

    return False


def _has_languages(resume: Resume) -> bool:
    """Check whether at least one meaningful language exists."""

    return any(
        language.name.strip()
        for language in resume.languages
    )


def _has_achievements(resume: Resume) -> bool:
    """Check whether at least one meaningful achievement exists."""

    return any(
        achievement.title.strip()
        for achievement in resume.achievements
    )


SECTION_CHECKERS = {
    "personal_information": _has_personal_information,
    "summary": _has_summary,
    "experience": _has_experience,
    "education": _has_education,
    "skills": _has_skills,
    "projects": _has_projects,
    "certifications": _has_certifications,
    "languages": _has_languages,
    "achievements": _has_achievements,
}


def calculate_completion(resume: Resume) -> Dict[str, object]:
    """
    Calculate the overall resume completion score.

    Returns:
        Dictionary containing:
        - overall_percentage
        - section_scores
        - completed_sections
        - incomplete_sections
        - next_steps
    """

    section_scores: Dict[str, int] = {}
    completed_sections: List[str] = []
    incomplete_sections: List[str] = []

    total_score = 0

    for section, weight in COMPLETION_WEIGHTS.items():
        checker = SECTION_CHECKERS[section]
        completed = checker(resume)

        section_scores[section] = weight if completed else 0

        if completed:
            completed_sections.append(section)
            total_score += weight
        else:
            incomplete_sections.append(section)

    overall_percentage = round(total_score)

    next_steps = generate_next_steps(
        incomplete_sections,
        maximum_suggestions=3,
    )

    return {
        "overall_percentage": overall_percentage,
        "section_scores": section_scores,
        "completed_sections": completed_sections,
        "incomplete_sections": incomplete_sections,
        "next_steps": next_steps,
    }


def generate_next_steps(
    incomplete_sections: List[str],
    maximum_suggestions: int = 3,
) -> List[str]:
    """Generate prioritized suggestions for incomplete sections."""

    suggestions = {
        "personal_information": (
            "Complete your name and at least one reliable contact method."
        ),
        "summary": (
            "Add a concise professional summary describing your experience "
            "and target career direction."
        ),
        "experience": (
            "Add relevant work experience with clear responsibilities "
            "and accomplishments."
        ),
        "education": (
            "Add your degree, field of study, and educational institution."
        ),
        "skills": (
            "Add at least three relevant technical or professional skills."
        ),
        "projects": (
            "Add at least one meaningful project with technologies, "
            "responsibilities, or outcomes."
        ),
        "certifications": (
            "Add relevant certifications if you have earned any."
        ),
        "languages": (
            "Add languages you can professionally communicate in."
        ),
        "achievements": (
            "Add relevant awards, achievements, or recognitions if available."
        ),
    }

    return [
        suggestions[section]
        for section in incomplete_sections[:maximum_suggestions]
    ]


def get_section_completion(
    resume: Resume,
) -> Dict[str, bool]:
    """Return a simple completion status for every section."""

    return {
        section: checker(resume)
        for section, checker in SECTION_CHECKERS.items()
    }
