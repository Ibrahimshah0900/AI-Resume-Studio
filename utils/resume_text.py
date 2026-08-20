
from __future__ import annotations
from utils.data_models import Resume

def resume_to_text(resume: Resume) -> str:
    """Convert a structured Resume model into readable ATS text."""
    parts: list[str] = []
    personal = resume.personal_info

    for value in [
        personal.full_name, personal.professional_title,
        personal.email, personal.phone, personal.location,
        personal.linkedin, personal.github, personal.portfolio,
    ]:
        if value:
            parts.append(str(value))

    if resume.summary:
        parts.append("SUMMARY")
        parts.append(resume.summary)

    if resume.skills:
        parts.append("SKILLS")
        parts.append(", ".join(resume.skills))

    if resume.experience:
        parts.append("EXPERIENCE")
        for item in resume.experience:
            for field in ["job_title", "company", "location", "start_date", "end_date", "description"]:
                value = getattr(item, field, "")
                if value:
                    parts.append(str(value))
            if item.bullet_points:
                for bullet in item.bullet_points:
                    parts.append(f"  • {bullet}")

    if resume.education:
        parts.append("EDUCATION")
        for item in resume.education:
            for field in ["degree", "field_of_study", "institution", "location", "start_date", "end_date", "grade"]:
                value = getattr(item, field, "")
                if value:
                    parts.append(str(value))

    if resume.projects:
        parts.append("PROJECTS")
        for item in resume.projects:
            for field in ["name", "description", "technologies", "project_url", "github_url"]:
                value = getattr(item, field, "")
                if value:
                    parts.append(str(value))

    if resume.certifications:
        parts.append("CERTIFICATIONS")
        for item in resume.certifications:
            parts.append(str(item.name))

    if resume.languages:
        parts.append("LANGUAGES")
        for item in resume.languages:
            parts.append(f"{item.name} - {item.proficiency}")

    if resume.achievements:
        parts.append("ACHIEVEMENTS")
        for item in resume.achievements:
            parts.append(str(item.title))

    return "\n".join(parts)

def resume_to_sections(resume: Resume) -> dict:
    """Convert a Resume model into ATS section data."""
    return {
        "summary": resume.summary,
        "experience": [exp.model_dump() for exp in resume.experience],
        "education": [edu.model_dump() for edu in resume.education],
        "skills": resume.skills,
        "projects": [proj.model_dump() for proj in resume.projects],
        "certifications": [cert.model_dump() for cert in resume.certifications],
        "languages": [lang.model_dump() for lang in resume.languages],
        "achievements": [ach.model_dump() for ach in resume.achievements],
    }
