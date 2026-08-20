
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class TemplateMetadata:
    template_id: str
    name: str
    description: str
    category: str
    ats_friendly: bool
    recommended_for: List[str]


TEMPLATES: Dict[str, TemplateMetadata] = {
    "ats_minimal": TemplateMetadata(
        template_id="ats_minimal",
        name="ATS Minimal",
        description="Clean single-column resume layout designed for readability and ATS compatibility.",
        category="ATS",
        ats_friendly=True,
        recommended_for=["Corporate applications", "ATS-heavy hiring systems", "General professional resumes"],
    ),
    "modern_professional": TemplateMetadata(
        template_id="modern_professional",
        name="Modern Professional",
        description="Contemporary professional layout with clear visual hierarchy.",
        category="Professional",
        ats_friendly=True,
        recommended_for=["Business roles", "Professional services", "Experienced candidates"],
    ),
    "ai_tech": TemplateMetadata(
        template_id="ai_tech",
        name="AI / Tech Professional",
        description="Technology-focused layout emphasizing technical skills, projects, and engineering experience.",
        category="Technology",
        ats_friendly=True,
        recommended_for=["Software Engineers", "Machine Learning Engineers", "Data Scientists", "AI / Computer Vision roles"],
    ),
    "classic_professional": TemplateMetadata(
        template_id="classic_professional",
        name="Classic Professional",
        description="Traditional resume structure with conservative typography and strong section hierarchy.",
        category="Classic",
        ats_friendly=True,
        recommended_for=["Traditional industries", "Academic applications", "Experienced professionals"],
    ),
    "student_graduate": TemplateMetadata(
        template_id="student_graduate",
        name="Student / Graduate",
        description="Education and project-oriented layout designed for students and early-career candidates.",
        category="Graduate",
        ats_friendly=True,
        recommended_for=["Students", "Recent graduates", "Internship applications", "Entry-level roles"],
    ),
}


DEFAULT_TEMPLATE_ID = "ats_minimal"


def list_templates() -> List[TemplateMetadata]:
    return list(TEMPLATES.values())


def get_template(template_id: str) -> TemplateMetadata:
    if template_id not in TEMPLATES:
        available = ", ".join(sorted(TEMPLATES))
        raise ValueError(f"Unknown template '{template_id}'. Available templates: {available}")
    return TEMPLATES[template_id]


def validate_template_id(template_id: str) -> bool:
    return template_id in TEMPLATES


def render_resume_data(resume_data: Dict[str, Any], template_id: str = DEFAULT_TEMPLATE_ID) -> Dict[str, Any]:
    template = get_template(template_id)
    if not isinstance(resume_data, dict):
        raise TypeError("resume_data must be a dictionary.")

    personal_info = resume_data.get("personal_info", {})

    return {
        "template": {
            "id": template.template_id,
            "name": template.name,
            "category": template.category,
            "ats_friendly": template.ats_friendly,
        },
        "personal_info": dict(personal_info),
        "summary": resume_data.get("summary", ""),
        "experience": list(resume_data.get("experience", [])),
        "education": list(resume_data.get("education", [])),
        "skills": list(resume_data.get("skills", [])),
        "projects": list(resume_data.get("projects", [])),
        "certifications": list(resume_data.get("certifications", [])),
        "languages": list(resume_data.get("languages", [])),
        "achievements": list(resume_data.get("achievements", [])),
        "awards": list(resume_data.get("awards", [])),
    }


def get_template_summary() -> List[Dict[str, Any]]:
    return [
        {
            "id": template.template_id,
            "name": template.name,
            "description": template.description,
            "category": template.category,
            "ats_friendly": template.ats_friendly,
            "recommended_for": template.recommended_for,
        }
        for template in list_templates()
    ]
