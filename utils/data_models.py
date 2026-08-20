
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, EmailStr


class PersonalInfo(BaseModel):
    """Basic contact and identity information."""

    model_config = ConfigDict(validate_assignment=True)

    full_name: str = ""
    professional_title: str = ""
    email: Optional[EmailStr] = None
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    github: str = ""
    portfolio: str = ""


class WorkExperience(BaseModel):
    """A single professional work experience entry."""

    model_config = ConfigDict(validate_assignment=True)

    job_title: str = ""
    company: str = ""
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    currently_working: bool = False
    description: str = ""
    bullet_points: List[str] = Field(default_factory=list)


class Education(BaseModel):
    """A single education entry."""

    model_config = ConfigDict(validate_assignment=True)

    degree: str = ""
    field_of_study: str = ""
    institution: str = ""
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    grade: str = ""
    description: str = ""


class Project(BaseModel):
    """A single resume project."""

    model_config = ConfigDict(validate_assignment=True)

    name: str = ""
    description: str = ""
    technologies: List[str] = Field(default_factory=list)
    project_url: str = ""
    github_url: str = ""
    bullet_points: List[str] = Field(default_factory=list)


class Certification(BaseModel):
    """A professional certification."""

    model_config = ConfigDict(validate_assignment=True)

    name: str = ""
    issuing_organization: str = ""
    issue_date: str = ""
    expiration_date: str = ""
    credential_id: str = ""
    credential_url: str = ""


class Language(BaseModel):
    """A spoken or written language."""

    model_config = ConfigDict(validate_assignment=True)

    name: str = ""
    proficiency: str = ""


class Achievement(BaseModel):
    """An achievement, award, or recognition."""

    model_config = ConfigDict(validate_assignment=True)

    title: str = ""
    organization: str = ""
    date: str = ""
    description: str = ""


class Resume(BaseModel):
    """Complete structured resume."""

    model_config = ConfigDict(validate_assignment=True)

    personal_info: PersonalInfo = Field(default_factory=PersonalInfo)

    summary: str = ""

    experience: List[WorkExperience] = Field(default_factory=list)

    education: List[Education] = Field(default_factory=list)

    skills: List[str] = Field(default_factory=list)

    projects: List[Project] = Field(default_factory=list)

    certifications: List[Certification] = Field(default_factory=list)

    languages: List[Language] = Field(default_factory=list)

    achievements: List[Achievement] = Field(default_factory=list)

    custom_sections: dict[str, str] = Field(default_factory=dict)


class ResumeMetadata(BaseModel):
    """Metadata used to manage resume versions."""

    model_config = ConfigDict(validate_assignment=True)

    resume_id: str = ""
    title: str = "Untitled Resume"
    version: int = 1
    created_at: str = ""
    updated_at: str = ""
    template_name: str = "ATS Minimal"


def create_empty_resume() -> Resume:
    """Return a clean empty resume."""

    return Resume()


def create_sample_resume() -> Resume:
    """Return realistic sample data for development and testing."""

    return Resume(
        personal_info=PersonalInfo(
            full_name="Alex Morgan",
            professional_title="Machine Learning Engineer",
            email="alex.morgan@example.com",
            phone="+1 555-0100",
            location="New York, NY",
            linkedin="https://www.linkedin.com/in/alexmorgan",
            github="https://github.com/alexmorgan",
            portfolio="https://alexmorgan.dev",
        ),
        summary=(
            "Machine Learning Engineer with experience building "
            "data-driven applications using Python, scikit-learn, "
            "and computer vision techniques."
        ),
        experience=[
            WorkExperience(
                job_title="Machine Learning Engineer",
                company="Example Technologies",
                location="New York, NY",
                start_date="2024-01",
                end_date="Present",
                currently_working=True,
                bullet_points=[
                    "Developed machine learning pipelines using Python and scikit-learn.",
                    "Built computer vision prototypes using OpenCV.",
                ],
            )
        ],
        education=[
            Education(
                degree="Bachelor of Science",
                field_of_study="Computer Science",
                institution="Example University",
                location="New York, NY",
                start_date="2020",
                end_date="2024",
            )
        ],
        skills=[
            "Python",
            "Machine Learning",
            "Scikit-learn",
            "OpenCV",
            "Pandas",
            "SQL",
            "Git",
        ],
        projects=[
            Project(
                name="Resume Intelligence Platform",
                description=(
                    "An application for resume parsing, ATS analysis, "
                    "and job matching."
                ),
                technologies=[
                    "Python",
                    "Streamlit",
                    "Scikit-learn",
                ],
                bullet_points=[
                    "Built a modular resume analysis pipeline.",
                    "Implemented keyword-based job matching.",
                ],
            )
        ],
        certifications=[
            Certification(
                name="Machine Learning Certificate",
                issuing_organization="Example Academy",
                issue_date="2025",
            )
        ],
        languages=[
            Language(
                name="English",
                proficiency="Professional",
            )
        ],
        achievements=[
            Achievement(
                title="Academic Excellence Award",
                organization="Example University",
                date="2024",
                description="Recognized for outstanding academic performance.",
            )
        ],
    )
