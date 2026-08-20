
from __future__ import annotations
from html import escape
from typing import Any, Dict, Iterable
from utils.template_engine import DEFAULT_TEMPLATE_ID, get_template, render_resume_data

def _safe(value: Any) -> str:
    if value is None:
        return ""
    return escape(str(value))

def _join_values(values: Iterable[Any]) -> str:
    return ", ".join(_safe(value) for value in values if value)

def _render_personal_info(personal_info: Dict[str, Any]) -> str:
    name = _safe(personal_info.get("full_name") or personal_info.get("name", ""))
    email = _safe(personal_info.get("email", ""))
    phone = _safe(personal_info.get("phone", ""))
    location = _safe(personal_info.get("location", ""))

    contact_parts = [value for value in [email, phone, location] if value]
    contact_html = " | ".join(contact_parts)

    return f"""
    <header class="resume-header">
        <h1>{name}</h1>
        <div class="contact">{contact_html}</div>
    </header>
    """

def _render_summary(summary: str) -> str:
    if not summary.strip():
        return ""
    return f"""
    <section>
        <h2>Professional Summary</h2>
        <p>{_safe(summary)}</p>
    </section>
    """

def _render_experience(experience: list) -> str:
    if not experience:
        return ""

    items = []
    for item in experience:
        title = _safe(item.get("job_title") or item.get("title") or "")
        company = _safe(item.get("company") or item.get("organization") or "")
        location = _safe(item.get("location", ""))
        start = _safe(item.get("start_date", ""))
        end = _safe(item.get("end_date", ""))

        dates = ""
        if start or end:
            dates = f"{start} - {end}".strip(" -")

        # Handle bullet points properly
        bullet_points = item.get("bullet_points", [])
        description = item.get("description", "")
        
        description_html = ""

        # Render bullet points as proper HTML list
        if bullet_points:
            bullets = "".join(f"<li>{_safe(bullet)}</li>" for bullet in bullet_points if bullet)
            if bullets:
                description_html = f"<ul>{bullets}</ul>"
        elif description:
            description_html = f"<p>{_safe(description)}</p>"

        items.append(f"""
            <article class="experience-item">
                <div class="item-heading">
                    <strong>{title}</strong>
                    <span>{dates}</span>
                </div>
                <div class="item-subheading">
                    {company}
                    {f" — {location}" if location else ""}
                </div>
                {description_html}
            </article>
            """)

    return f"""
    <section>
        <h2>Experience</h2>
        {''.join(items)}
    </section>
    """

def _render_education(education: list) -> str:
    if not education:
        return ""

    items = []
    for item in education:
        degree = _safe(item.get("degree") or item.get("qualification") or "")
        institution = _safe(item.get("institution") or item.get("school") or item.get("university") or "")
        location = _safe(item.get("location", ""))
        year = _safe(item.get("graduation_date") or item.get("year") or "")
        start = _safe(item.get("start_date", ""))
        end = _safe(item.get("end_date", ""))

        dates = ""
        if start or end:
            dates = f"{start} - {end}".strip(" -")
        if not dates and year:
            dates = year

        items.append(f"""
            <article class="education-item">
                <div class="item-heading">
                    <strong>{degree}</strong>
                    <span>{dates}</span>
                </div>
                <div class="item-subheading">
                    {institution}
                    {f" — {location}" if location else ""}
                </div>
            </article>
            """)

    return f"""
    <section>
        <h2>Education</h2>
        {''.join(items)}
    </section>
    """

def _render_skills(skills: list) -> str:
    if not skills:
        return ""
    
    # Render skills as styled tags/spans
    skill_tags = "".join(f'<span>{_safe(skill)}</span> ' for skill in skills if skill)
    
    return f"""
    <section>
        <h2>Technical Skills</h2>
        <p class="skills">{skill_tags}</p>
    </section>
    """

def _render_projects(projects: list) -> str:
    if not projects:
        return ""

    items = []
    for item in projects:
        name = _safe(item.get("name") or item.get("title") or "")
        description = _safe(item.get("description") or "")
        technologies = item.get("technologies", [])
        bullet_points = item.get("bullet_points", [])

        technology_html = ""
        if technologies:
            technology_html = f"<p class='technologies'><strong>Technologies:</strong> {_join_values(technologies)}</p>"
        
        bullets_html = ""
        if bullet_points:
            bullets = "".join(f"<li>{_safe(bullet)}</li>" for bullet in bullet_points if bullet)
            if bullets:
                bullets_html = f"<ul>{bullets}</ul>"

        items.append(f"""
            <article class="project-item">
                <div class="item-heading">
                    <strong>{name}</strong>
                </div>
                <p>{description}</p>
                {technology_html}
                {bullets_html}
            </article>
            """)

    return f"""
    <section>
        <h2>Projects</h2>
        {''.join(items)}
    </section>
    """

def _render_simple_section(title: str, values: list) -> str:
    if not values:
        return ""

    rendered = []
    for value in values:
        if isinstance(value, dict):
            text = ", ".join(_safe(v) for v in value.values() if v)
        else:
            text = _safe(value)
        if text:
            rendered.append(f"<li>{text}</li>")

    if not rendered:
        return ""

    return f"""
    <section>
        <h2>{_safe(title)}</h2>
        <ul>
            {''.join(rendered)}
        </ul>
    </section>
    """

def _template_css(template_id: str) -> str:
    base = """
    @page { size: A4; margin: 16mm; }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { margin: 0; font-family: Arial, Helvetica, sans-serif; color: #202124; background: white; font-size: 10.5pt; line-height: 1.5; }
    .resume { max-width: 800px; margin: 0 auto; padding: 8px; }
    .resume-header { margin-bottom: 16px; }
    h1 { margin: 0 0 4px; font-size: 24pt; line-height: 1.15; }
    h2 { font-size: 12pt; text-transform: uppercase; letter-spacing: 0.7px; margin: 14px 0 6px; padding-bottom: 4px; border-bottom: 1.5px solid #d8d8d8; }
    p { margin: 4px 0; }
    ul { margin: 4px 0 0 18px; padding: 0; list-style-type: disc; }
    li { margin-bottom: 2px; font-size: 10pt; line-height: 1.4; }
    .contact { color: #555; font-size: 9.5pt; margin-bottom: 10px; }
    .item-heading { display: flex; justify-content: space-between; gap: 12px; margin-top: 8px; }
    .item-heading strong { font-size: 11pt; white-space: normal; word-wrap: break-word; }
    .item-heading span { color: #666; white-space: nowrap; min-width: 80px; text-align: right; }
    .item-subheading { color: #444; margin-top: 2px; font-size: 10pt; }
    .experience-item, .education-item, .project-item { margin-bottom: 10px; }
    .skills { margin-top: 4px; }
    .skills span { display: inline-block; background: #f0f0f0; padding: 2px 10px; border-radius: 4px; margin: 2px 4px 2px 0; font-size: 10pt; }
    .technologies { color: #555; font-size: 9.5pt; margin-top: 2px; }
    """

    variants = {
        "ats_minimal": ".resume-header { border-bottom: 2px solid #222; padding-bottom: 8px; }",
        "modern_professional": "body { color: #243447; } .resume-header { border-left: 5px solid #2563eb; padding-left: 14px; } h2 { color: #2563eb; border-bottom-color: #bfdbfe; }",
        "ai_tech": "body { color: #172033; } .resume-header { background: #f3f6fb; padding: 16px; border-radius: 6px; } h2 { color: #174ea6; border-bottom-color: #9db9e8; } .technologies { color: #174ea6; }",
        "classic_professional": "body { font-family: Georgia, 'Times New Roman', serif; color: #222; } h1, h2 { font-family: Arial, Helvetica, sans-serif; }",
        "student_graduate": ".resume-header { border-bottom: 1px solid #999; padding-bottom: 8px; } h2 { color: #374151; }",
    }

    return base + variants.get(template_id, variants["ats_minimal"])

def render_resume_html(resume_data: Dict[str, Any], template_id: str = DEFAULT_TEMPLATE_ID) -> str:
    normalized = render_resume_data(resume_data, template_id=template_id)
    template = get_template(template_id)

    css = _template_css(template.template_id)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_safe(normalized["personal_info"].get("full_name") or normalized["personal_info"].get("name", "Resume"))}</title>
<style>{css}</style>
</head>
<body>
<div class="resume">
{_render_personal_info(normalized["personal_info"])}
{_render_summary(normalized["summary"])}
{_render_experience(normalized["experience"])}
{_render_education(normalized["education"])}
{_render_skills(normalized["skills"])}
{_render_projects(normalized["projects"])}
{_render_simple_section("Certifications", normalized["certifications"])}
{_render_simple_section("Languages", normalized["languages"])}
{_render_simple_section("Achievements", normalized["achievements"])}
{_render_simple_section("Awards", normalized["awards"])}
</div>
</body>
</html>
"""
