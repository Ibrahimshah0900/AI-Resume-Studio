
from __future__ import annotations

import re
from typing import Any, Dict, List

from utils.keyword_extractor import compare_keywords
from utils.skill_extractor import compare_skills


ATS_WEIGHTS = {
    "contact_information": 10,
    "section_completeness": 20,
    "keyword_match": 25,
    "skills_match": 20,
    "readability": 15,
    "formatting": 10,
}


def analyze_contact_information(resume_text: str) -> Dict[str, Any]:
    if not isinstance(resume_text, str):
        resume_text = ""

    email_found = bool(re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", resume_text))
    phone_found = bool(re.search(r"(?:\+?\d[\d\s().-]{7,}\d)", resume_text))
    lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
    name_found = len(lines) > 0

    checks = {"name": name_found, "email": email_found, "phone": phone_found}
    score = sum(checks.values()) / len(checks) * ATS_WEIGHTS["contact_information"]

    return {"score": round(score, 2), "max_score": ATS_WEIGHTS["contact_information"], "checks": checks}


def analyze_section_completeness(resume_sections: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(resume_sections, dict):
        resume_sections = {}

    important_sections = ["summary", "experience", "education", "skills", "projects"]
    checks = {}

    for section in important_sections:
        value = resume_sections.get(section)
        if isinstance(value, str):
            checks[section] = bool(value.strip())
        elif isinstance(value, list):
            checks[section] = len(value) > 0
        elif isinstance(value, dict):
            checks[section] = bool(value)
        else:
            checks[section] = bool(value)

    completed = sum(checks.values())
    score = completed / len(checks) * ATS_WEIGHTS["section_completeness"]

    return {
        "score": round(score, 2),
        "max_score": ATS_WEIGHTS["section_completeness"],
        "checks": checks,
        "completed_sections": completed,
        "total_sections": len(checks),
    }


def analyze_keyword_match(resume_text: str, job_description: str) -> Dict[str, Any]:
    if not job_description.strip():
        return {
            "score": ATS_WEIGHTS["keyword_match"],
            "max_score": ATS_WEIGHTS["keyword_match"],
            "match_percentage": 100.0,
            "matching": [],
            "missing": [],
            "additional": [],
            "job_description_provided": False,
        }

    comparison = compare_keywords(resume_text, job_description, top_n=30)
    job_keywords = set(comparison["matching"]) | set(comparison["missing"])
    matching = set(comparison["matching"])

    match_percentage = (len(matching) / len(job_keywords) * 100) if job_keywords else 0.0
    score = match_percentage / 100 * ATS_WEIGHTS["keyword_match"]

    return {
        "score": round(score, 2),
        "max_score": ATS_WEIGHTS["keyword_match"],
        "match_percentage": round(match_percentage, 2),
        "matching": sorted(matching),
        "missing": sorted(comparison["missing"]),
        "additional": sorted(comparison["additional"]),
        "job_description_provided": True,
    }


def analyze_skill_match(resume_text: str, job_description: str) -> Dict[str, Any]:
    if not job_description.strip():
        return {
            "score": ATS_WEIGHTS["skills_match"],
            "max_score": ATS_WEIGHTS["skills_match"],
            "match_percentage": 100.0,
            "matching": [],
            "missing": [],
            "additional": [],
            "job_description_provided": False,
        }

    comparison = compare_skills(resume_text, job_description)
    matching = set(comparison.get("matching", []))
    missing = set(comparison.get("missing", []))
    total_job_skills = len(matching) + len(missing)

    match_percentage = (len(matching) / total_job_skills * 100) if total_job_skills else 0.0
    score = match_percentage / 100 * ATS_WEIGHTS["skills_match"]

    return {
        "score": round(score, 2),
        "max_score": ATS_WEIGHTS["skills_match"],
        "match_percentage": round(match_percentage, 2),
        "matching": sorted(matching),
        "missing": sorted(missing),
        "additional": sorted(comparison.get("additional", [])),
        "job_description_provided": True,
    }


def analyze_readability(resume_text: str) -> Dict[str, Any]:
    text = resume_text.strip()
    if not text:
        return {
            "score": 0.0,
            "max_score": ATS_WEIGHTS["readability"],
            "word_count": 0,
            "average_sentence_length": 0.0,
            "checks": {},
        }

    words = re.findall(r"\b[\w+#.-]+\b", text)
    sentences = [sentence.strip() for sentence in re.split(r"[.!?]+", text) if sentence.strip()]

    word_count = len(words)
    average_sentence_length = word_count / len(sentences) if sentences else float(word_count)

    checks = {
        "has_content": word_count >= 20,
        "reasonable_length": 20 <= word_count <= 1500,
        "reasonable_sentence_length": average_sentence_length <= 30,
    }
    score = sum(checks.values()) / len(checks) * ATS_WEIGHTS["readability"]

    return {
        "score": round(score, 2),
        "max_score": ATS_WEIGHTS["readability"],
        "word_count": word_count,
        "average_sentence_length": round(average_sentence_length, 2),
        "checks": checks,
    }


def analyze_formatting(resume_text: str) -> Dict[str, Any]:
    text = resume_text.strip()
    if not text:
        return {"score": 0.0, "max_score": ATS_WEIGHTS["formatting"], "checks": {}}

    non_empty_lines = [line.strip() for line in text.splitlines() if line.strip()]
    checks = {
        "has_multiple_lines": len(non_empty_lines) >= 5,
        "reasonable_line_length": all(len(line) <= 180 for line in non_empty_lines),
        "no_excessive_blank_lines": "\n\n\n" not in text,
    }
    score = sum(checks.values()) / len(checks) * ATS_WEIGHTS["formatting"]

    return {
        "score": round(score, 2),
        "max_score": ATS_WEIGHTS["formatting"],
        "checks": checks,
    }


def generate_recommendations(analysis: Dict[str, Any]) -> List[str]:
    recommendations = []

    contact = analysis["contact_information"]
    for field, present in contact["checks"].items():
        if not present:
            recommendations.append(f"Add your {field} to the resume.")

    sections = analysis["section_completeness"]
    for section, present in sections["checks"].items():
        if not present:
            recommendations.append(f"Consider adding a {section.replace('_', ' ')} section.")

    keyword_data = analysis["keyword_match"]
    if keyword_data["job_description_provided"] and keyword_data["match_percentage"] < 60:
        recommendations.append("Add more relevant keywords from the job description where they truthfully match your experience.")

    skill_data = analysis["skills_match"]
    if skill_data["job_description_provided"] and skill_data["missing"]:
        recommendations.append("Review the missing job skills and add only those you genuinely possess.")

    readability = analysis["readability"]
    if not readability["checks"].get("reasonable_sentence_length", True):
        recommendations.append("Shorten long sentences and bullet points for easier scanning.")

    formatting = analysis["formatting"]
    if formatting["score"] < formatting["max_score"]:
        recommendations.append("Review resume spacing and line formatting for consistent readability.")

    if not recommendations:
        recommendations.append("Your resume currently meets the baseline checks. Continue tailoring it to the target role.")

    return recommendations


def analyze_resume_ats(
    resume_text: str,
    resume_sections: Dict[str, Any] | None = None,
    job_description: str = "",
) -> Dict[str, Any]:
    if not isinstance(resume_text, str):
        resume_text = ""
    if resume_sections is None:
        resume_sections = {}

    breakdown = {
        "contact_information": analyze_contact_information(resume_text),
        "section_completeness": analyze_section_completeness(resume_sections),
        "keyword_match": analyze_keyword_match(resume_text, job_description),
        "skills_match": analyze_skill_match(resume_text, job_description),
        "readability": analyze_readability(resume_text),
        "formatting": analyze_formatting(resume_text),
    }

    total_score = sum(component["score"] for component in breakdown.values())
    total_max_score = sum(component["max_score"] for component in breakdown.values())
    percentage = (total_score / total_max_score * 100) if total_max_score else 0.0

    analysis = {
        "score": round(percentage, 2),
        "score_out_of_100": round(percentage),
        "breakdown": breakdown,
        **breakdown,
    }
    analysis["recommendations"] = generate_recommendations(analysis)

    return analysis
