
from __future__ import annotations
import streamlit as st
import random
from utils.completion_engine import calculate_completion
from utils.data_models import (
    Education, PersonalInfo, Project, Resume, WorkExperience,
    Certification, Language, Achievement
)
from utils.resume_builder_core import (
    add_education, add_experience, add_project, add_skill,
    remove_education, remove_experience, remove_project, remove_skill,
    update_personal_info, update_summary
)

# Sample resume data for 1-click demo
SAMPLE_RESUME = {
    "personal_info": {
        "full_name": "Alex Morgan",
        "professional_title": "Senior Machine Learning Engineer",
        "email": "alex.morgan@example.com",
        "phone": "+1 555 123 4567",
        "location": "San Francisco, CA",
        "linkedin": "linkedin.com/in/alexmorgan",
        "github": "github.com/alexmorgan",
        "portfolio": "alexmorgan.dev"
    },
    "summary": "Senior Machine Learning Engineer with 5+ years of experience building and deploying production-grade ML systems. Expertise in computer vision, NLP, and MLOps. Passionate about building scalable AI solutions that solve real-world problems.",
    "experience": [
        {
            "job_title": "Senior Machine Learning Engineer",
            "company": "TechSolutions Inc.",
            "location": "San Francisco, CA",
            "start_date": "2022-01",
            "end_date": "Present",
            "currently_working": True,
            "description": "",
            "bullet_points": [
                "Designed and deployed a computer vision system processing 10M+ images daily with 98.5% accuracy",
                "Led a team of 5 engineers to build an MLOps pipeline reducing model deployment time by 70%",
                "Implemented real-time anomaly detection system saving $2M annually in operational costs",
                "Optimized inference latency from 500ms to 50ms using model quantization and distillation"
            ]
        },
        {
            "job_title": "Machine Learning Engineer",
            "company": "DataFlow Labs",
            "location": "New York, NY",
            "start_date": "2020-06",
            "end_date": "2021-12",
            "currently_working": False,
            "description": "",
            "bullet_points": [
                "Built NLP pipeline for sentiment analysis achieving 92% F1 score on customer feedback data",
                "Developed A/B testing framework for ML models increasing feature adoption by 40%",
                "Created data validation framework reducing data quality issues by 85%"
            ]
        }
    ],
    "education": [
        {
            "degree": "Master of Science",
            "field_of_study": "Computer Science - AI Specialization",
            "institution": "Stanford University",
            "location": "Stanford, CA",
            "start_date": "2018-09",
            "end_date": "2020-06",
            "grade": "3.9 GPA"
        },
        {
            "degree": "Bachelor of Science",
            "field_of_study": "Computer Engineering",
            "institution": "MIT",
            "location": "Cambridge, MA",
            "start_date": "2014-09",
            "end_date": "2018-06",
            "grade": "3.8 GPA"
        }
    ],
    "skills": [
        "Python", "PyTorch", "TensorFlow", "Scikit-learn", "OpenCV",
        "NLP", "Computer Vision", "MLOps", "Docker", "Kubernetes",
        "AWS", "GCP", "SQL", "NoSQL", "Git", "CI/CD", "Streamlit"
    ],
    "projects": [
        {
            "name": "AI Resume Studio",
            "description": "Full-stack AI-powered resume platform with ATS analysis, job matching, and intelligent improvement suggestions",
            "technologies": ["Python", "Streamlit", "NLP", "Computer Vision", "ML"],
            "bullet_points": [
                "Built end-to-end resume parsing and analysis pipeline supporting PDF, DOCX, and image formats",
                "Implemented ATS compatibility scoring with 95%+ accuracy against major ATS systems"
            ]
        },
        {
            "name": "Real-time Object Detection System",
            "description": "Production-ready object detection system for retail inventory management",
            "technologies": ["PyTorch", "YOLO", "FastAPI", "Docker"],
            "bullet_points": [
                "Achieved 94% mAP on custom retail dataset with 30 FPS inference",
                "Deployed as microservice handling 10K+ requests daily"
            ]
        }
    ],
    "certifications": [
        {"name": "AWS Certified Machine Learning Specialty"},
        {"name": "Deep Learning Specialization - Coursera"}
    ],
    "languages": [
        {"name": "English", "proficiency": "Native"},
        {"name": "Spanish", "proficiency": "Professional"}
    ],
    "achievements": [
        {"title": "Best Paper Award - NeurIPS 2021"},
        {"title": "Google AI Research Grant 2022"}
    ],
    "awards": [
        {"title": "TechCrunch Disrupt 2023 Finalist"},
        {"title": "Forbes 30 Under 30 - AI Category"}
    ]
}

def load_sample_resume():
    """Load sample resume data into session state."""
    resume = Resume(
        personal_info=PersonalInfo(**SAMPLE_RESUME["personal_info"]),
        summary=SAMPLE_RESUME["summary"],
        experience=[WorkExperience(**exp) for exp in SAMPLE_RESUME["experience"]],
        education=[Education(**edu) for edu in SAMPLE_RESUME["education"]],
        skills=SAMPLE_RESUME["skills"],
        projects=[Project(**proj) for proj in SAMPLE_RESUME["projects"]],
        certifications=[Certification(**cert) for cert in SAMPLE_RESUME["certifications"]],
        languages=[Language(**lang) for lang in SAMPLE_RESUME["languages"]],
        achievements=[Achievement(**ach) for ach in SAMPLE_RESUME["achievements"]],
    )
    st.session_state.resume_data = resume
    st.session_state.resume_dirty = True
    return resume

def initialize_resume_state() -> None:
    if "resume_data" not in st.session_state:
        st.session_state.resume_data = Resume()

def initialize_section_toggles() -> None:
    """Initialize section toggle states."""
    if "show_summary" not in st.session_state:
        st.session_state.show_summary = True
    if "show_experience" not in st.session_state:
        st.session_state.show_experience = True
    if "show_education" not in st.session_state:
        st.session_state.show_education = True
    if "show_skills" not in st.session_state:
        st.session_state.show_skills = True
    if "show_projects" not in st.session_state:
        st.session_state.show_projects = True
    if "show_certifications" not in st.session_state:
        st.session_state.show_certifications = True
    if "show_languages" not in st.session_state:
        st.session_state.show_languages = True
    if "show_achievements" not in st.session_state:
        st.session_state.show_achievements = True
    if "show_awards" not in st.session_state:
        st.session_state.show_awards = True
    if "include_gpa" not in st.session_state:
        st.session_state.include_gpa = True

def move_experience_up(resume: Resume, index: int) -> Resume:
    """Move an experience entry up in the list."""
    if index > 0:
        resume.experience[index], resume.experience[index - 1] = resume.experience[index - 1], resume.experience[index]
        st.session_state.resume_dirty = True
    return resume

def move_experience_down(resume: Resume, index: int) -> Resume:
    """Move an experience entry down in the list."""
    if index < len(resume.experience) - 1:
        resume.experience[index], resume.experience[index + 1] = resume.experience[index + 1], resume.experience[index]
        st.session_state.resume_dirty = True
    return resume

def move_project_up(resume: Resume, index: int) -> Resume:
    """Move a project entry up in the list."""
    if index > 0:
        resume.projects[index], resume.projects[index - 1] = resume.projects[index - 1], resume.projects[index]
        st.session_state.resume_dirty = True
    return resume

def move_project_down(resume: Resume, index: int) -> Resume:
    """Move a project entry down in the list."""
    if index < len(resume.projects) - 1:
        resume.projects[index], resume.projects[index + 1] = resume.projects[index + 1], resume.projects[index]
        st.session_state.resume_dirty = True
    return resume

def render_section_toggles() -> None:
    """Render section toggle switches."""
    st.subheader("Section Toggles")
    st.caption("Toggle sections on/off for the current export")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.checkbox("Summary", value=st.session_state.show_summary, key="show_summary")
        st.checkbox("Experience", value=st.session_state.show_experience, key="show_experience")
        st.checkbox("Education", value=st.session_state.show_education, key="show_education")
    with col2:
        st.checkbox("Skills", value=st.session_state.show_skills, key="show_skills")
        st.checkbox("Projects", value=st.session_state.show_projects, key="show_projects")
        st.checkbox("Certifications", value=st.session_state.show_certifications, key="show_certifications")
    with col3:
        st.checkbox("Languages", value=st.session_state.show_languages, key="show_languages")
        st.checkbox("Achievements", value=st.session_state.show_achievements, key="show_achievements")
        st.checkbox("Awards", value=st.session_state.show_awards, key="show_awards")

def render_personal_information(resume: Resume) -> None:
    st.subheader("Personal Information")
    col1, col2 = st.columns(2)

    with col1:
        full_name = st.text_input("Full Name", value=resume.personal_info.full_name, key="personal_full_name")
        professional_title = st.text_input("Professional Title", value=resume.personal_info.professional_title, key="personal_title")
        email = st.text_input("Email", value=str(resume.personal_info.email) if resume.personal_info.email else "", key="personal_email")

    with col2:
        phone = st.text_input("Phone", value=resume.personal_info.phone, key="personal_phone")
        location = st.text_input("Location", value=resume.personal_info.location, key="personal_location")
        linkedin = st.text_input("LinkedIn URL", value=resume.personal_info.linkedin, key="personal_linkedin")

    github = st.text_input("GitHub URL", value=resume.personal_info.github, key="personal_github")
    portfolio = st.text_input("Portfolio URL", value=resume.personal_info.portfolio, key="personal_portfolio")

    if st.button("Save Personal Information", key="save_personal_information"):
        try:
            personal_info = PersonalInfo(
                full_name=full_name, professional_title=professional_title,
                email=email or None, phone=phone, location=location,
                linkedin=linkedin, github=github, portfolio=portfolio
            )
            update_personal_info(st.session_state.resume_data, personal_info)
            st.success("Personal information saved.")
        except Exception as exc:
            st.error(f"Unable to save personal information: {exc}")

def render_summary(resume: Resume) -> None:
    st.subheader("Professional Summary")
    
    summary = st.text_area(
        "Summary", 
        value=resume.summary, 
        height=120,
        placeholder="Write a concise professional summary describing your experience, strengths, and career direction.",
        key="resume_summary"
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Save Summary", key="save_summary"):
            update_summary(st.session_state.resume_data, summary)
            st.success("Professional summary saved.")
    with col2:
        if st.button("Enhance", key="enhance_summary"):
            enhanced = summary
            if "experienced" in enhanced:
                enhanced = enhanced.replace("experienced", "proven track record of excellence in")
            if "skills" in enhanced:
                enhanced = enhanced.replace("skills", "core competencies")
            if not any(word in enhanced.lower() for word in ["achieved", "delivered", "built", "led"]):
                enhanced = "Delivered impactful results. " + enhanced
            st.session_state.resume_data.summary = enhanced
            st.success("Summary enhanced! Save to keep changes.")
            st.rerun()

def render_experience(resume: Resume) -> None:
    st.subheader("Work Experience")

    exp_text = ""
    for exp in resume.experience:
        exp_text += f"{exp.job_title} at {exp.company}\n"
    
    if len(exp_text) > 500:
        st.warning("Long experience section may overflow to page 2")

    if resume.experience:
        for index, experience in enumerate(resume.experience):
            with st.expander(f"{experience.job_title or 'Experience'} — {experience.company or 'Company'}", expanded=False):
                st.write(f"**Location:** {experience.location or 'Not provided'}")
                if experience.start_date:
                    st.write(f"**Start:** {experience.start_date}")
                if experience.end_date:
                    st.write(f"**End:** {experience.end_date}")
                if experience.bullet_points:
                    for bullet in experience.bullet_points:
                        st.write(f"• {bullet}")
                
                col1, col2, col3, col4 = st.columns([3, 1, 0.8, 0.8])
                with col1:
                    if st.button("Remove", key=f"remove_experience_{index}"):
                        remove_experience(st.session_state.resume_data, index)
                        st.rerun()
                with col2:
                    if st.button("Rewrite", key=f"rewrite_experience_{index}"):
                        bullets = experience.bullet_points
                        new_bullets = []
                        for bullet in bullets:
                            if bullet.startswith("Worked on"):
                                bullet = bullet.replace("Worked on", "Spearheaded development of")
                            elif bullet.startswith("Responsible for"):
                                bullet = bullet.replace("Responsible for", "Owned and delivered")
                            elif bullet.startswith("Helped"):
                                bullet = bullet.replace("Helped", "Drove")
                            if not any(word in bullet for word in ["%", "increased", "reduced", "improved", "saved"]):
                                bullet += " resulting in significant business impact"
                            new_bullets.append(bullet)
                        experience.bullet_points = new_bullets
                        st.success("Bullets enhanced! Save to keep changes.")
                        st.rerun()
                with col3:
                    if st.button("▲", key=f"move_up_exp_{index}"):
                        move_experience_up(st.session_state.resume_data, index)
                        st.rerun()
                with col4:
                    if st.button("▼", key=f"move_down_exp_{index}"):
                        move_experience_down(st.session_state.resume_data, index)
                        st.rerun()

    with st.expander("Add Work Experience", expanded=False):
        job_title = st.text_input("Job Title", key="new_experience_job_title")
        company = st.text_input("Company", key="new_experience_company")
        location = st.text_input("Location", key="new_experience_location")

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.text_input("Start Date", key="new_experience_start", placeholder="YYYY-MM")
        with col2:
            end_date = st.text_input("End Date", key="new_experience_end", placeholder="YYYY-MM or Present")

        description = st.text_area("Description", key="new_experience_description")
        bullets_text = st.text_area("Bullet Points", placeholder="Enter one achievement or responsibility per line.", key="new_experience_bullets")

        if st.button("Add Experience", key="add_experience"):
            if not job_title.strip() or not company.strip():
                st.warning("Job title and company are required.")
            else:
                bullets = [b.strip() for b in bullets_text.splitlines() if b.strip()]
                experience = WorkExperience(
                    job_title=job_title, company=company, location=location,
                    start_date=start_date, end_date=end_date,
                    currently_working=end_date.strip().lower() == "present",
                    description=description, bullet_points=bullets
                )
                add_experience(st.session_state.resume_data, experience)
                st.success("Work experience added.")
                st.rerun()

def render_education(resume: Resume) -> None:
    st.subheader("Education")

    if resume.education:
        for index, education in enumerate(resume.education):
            with st.expander(f"{education.degree or 'Education'} — {education.institution or 'Institution'}", expanded=False):
                if education.field_of_study:
                    st.write(f"**Field:** {education.field_of_study}")
                if education.start_date:
                    st.write(f"**Start:** {education.start_date}")
                if education.end_date:
                    st.write(f"**End:** {education.end_date}")
                if st.button("Remove", key=f"remove_education_{index}"):
                    remove_education(st.session_state.resume_data, index)
                    st.rerun()

    with st.expander("Add Education", expanded=False):
        degree = st.text_input("Degree", key="new_education_degree")
        field_of_study = st.text_input("Field of Study", key="new_education_field")
        institution = st.text_input("Institution", key="new_education_institution")
        location = st.text_input("Location", key="new_education_location")

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.text_input("Start Date", key="new_education_start")
        with col2:
            end_date = st.text_input("End Date", key="new_education_end")

        grade = st.text_input("Grade", key="new_education_grade")
        description = st.text_area("Description", key="new_education_description")

        if st.button("Add Education", key="add_education"):
            if not degree.strip() and not institution.strip():
                st.warning("Please provide at least a degree or institution.")
            else:
                education = Education(
                    degree=degree, field_of_study=field_of_study,
                    institution=institution, location=location,
                    start_date=start_date, end_date=end_date,
                    grade=grade, description=description
                )
                add_education(st.session_state.resume_data, education)
                st.success("Education added.")
                st.rerun()

def render_skills(resume: Resume) -> None:
    st.subheader("Technical & Professional Skills")
    st.caption("Press Enter or comma to add skills")

    skills_text = st.text_input(
        "Add Skill", 
        placeholder="e.g. Python, Press Enter to add",
        key="new_skill_input"
    )
    
    if skills_text and (skills_text.endswith(",") or skills_text.endswith(" ")):
        skill = skills_text.rstrip(", ").strip()
        if skill:
            add_skill(st.session_state.resume_data, skill)
            st.rerun()

    if resume.skills:
        cols = st.columns(4)
        for i, skill in enumerate(resume.skills):
            with cols[i % 4]:
                if st.button(f"✕ {skill}", key=f"remove_skill_{i}"):
                    remove_skill(st.session_state.resume_data, skill)
                    st.rerun()
    else:
        st.info("No skills added yet. Start typing above!")

def render_projects(resume: Resume) -> None:
    st.subheader("Projects")

    if resume.projects:
        for index, project in enumerate(resume.projects):
            with st.expander(project.name or "Project", expanded=False):
                if project.description:
                    st.write(project.description)
                if project.technologies:
                    st.write("**Technologies:** " + ", ".join(project.technologies))
                if project.bullet_points:
                    for bullet in project.bullet_points:
                        st.write(f"• {bullet}")
                
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    if st.button("Remove", key=f"remove_project_{index}"):
                        remove_project(st.session_state.resume_data, index)
                        st.rerun()
                with col2:
                    if st.button("▲", key=f"move_up_proj_{index}"):
                        move_project_up(st.session_state.resume_data, index)
                        st.rerun()
                with col3:
                    if st.button("▼", key=f"move_down_proj_{index}"):
                        move_project_down(st.session_state.resume_data, index)
                        st.rerun()

    with st.expander("Add Project", expanded=False):
        name = st.text_input("Project Name", key="new_project_name")
        description = st.text_area("Project Description", key="new_project_description")
        technologies_text = st.text_input("Technologies", placeholder="Python, Streamlit, Scikit-learn", key="new_project_technologies")
        project_url = st.text_input("Project URL", key="new_project_url")
        github_url = st.text_input("GitHub URL", key="new_project_github")

        if st.button("Add Project", key="add_project"):
            if not name.strip():
                st.warning("Project name is required.")
            else:
                technologies = [t.strip() for t in technologies_text.split(",") if t.strip()]
                project = Project(
                    name=name, description=description,
                    technologies=technologies, project_url=project_url, github_url=github_url
                )
                add_project(st.session_state.resume_data, project)
                st.success("Project added.")
                st.rerun()

def render_resume_preview(resume: Resume) -> None:
    st.subheader("Live Resume Preview")
    info = resume.personal_info

    if info.full_name:
        st.markdown(f"# {info.full_name}")
    if info.professional_title:
        st.markdown(f"**{info.professional_title}**")

    contact_parts = [str(info.email) if info.email else "", info.phone, info.location]
    contact_line = " | ".join(part for part in contact_parts if part)
    if contact_line:
        st.caption(contact_line)

    if resume.summary:
        st.markdown("### Professional Summary")
        st.write(resume.summary)

    if resume.experience:
        st.markdown("### Experience")
        for experience in resume.experience:
            st.markdown(f"**{experience.job_title}** — {experience.company}")
            if experience.location:
                st.caption(experience.location)
            for bullet in experience.bullet_points:
                st.write(f"• {bullet}")

    if resume.education:
        st.markdown("### Education")
        for education in resume.education:
            title = " — ".join(item for item in [education.degree, education.field_of_study] if item)
            st.markdown(f"**{title or 'Education'}**")
            if education.institution:
                st.write(education.institution)

    if resume.skills:
        st.markdown("### Skills")
        st.write(", ".join(resume.skills))

    if resume.projects:
        st.markdown("### Projects")
        for project in resume.projects:
            st.markdown(f"**{project.name}**")
            if project.description:
                st.write(project.description)
            if project.technologies:
                st.caption("Technologies: " + ", ".join(project.technologies))

def render_resume_builder() -> None:
    initialize_resume_state()
    initialize_section_toggles()
    resume: Resume = st.session_state.resume_data

    st.title("AI Resume Studio")
    st.caption("Build your professional resume step by step.")

    completion = calculate_completion(resume)
    percentage = completion["overall_percentage"]
    st.progress(percentage / 100, text=f"Resume Completion: {percentage}%")

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("⚡ Pre-fill Sample Data", type="primary", use_container_width=True):
            load_sample_resume()
            st.success("Sample resume loaded! Scroll down to see the data.")
            st.rerun()

    left_column, right_column = st.columns([1.15, 0.85])

    with left_column:
        render_personal_information(resume)
        st.divider()
        render_section_toggles()
        st.divider()
        render_summary(resume)
        st.divider()
        render_experience(resume)
        st.divider()
        render_education(resume)
        st.divider()
        render_skills(resume)
        st.divider()
        render_projects(resume)

    with right_column:
        render_resume_preview(resume)
        if completion["next_steps"]:
            st.divider()
            st.subheader("Next Best Steps")
            for step in completion["next_steps"]:
                st.info(step)
