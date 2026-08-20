
from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import List


@dataclass
class ImprovementResult:
    original_text: str
    suggestions: List[str] = field(default_factory=list)
    detected_issues: List[str] = field(default_factory=list)
    action_verbs_found: List[str] = field(default_factory=list)
    metrics_found: List[str] = field(default_factory=list)
    technical_terms_found: List[str] = field(default_factory=list)
    score: float = 0.0


WEAK_PHRASES = {
    "worked on": "Describe what you specifically built, improved, analyzed, or delivered.",
    "responsible for": "Replace with a specific action describing what you actually did.",
    "helped with": "Explain your direct contribution instead of using a vague helper phrase.",
    "worked with": "Specify how you used the technology, tool, or process.",
    "participated in": "Describe your concrete contribution to the project.",
    "involved in": "Replace with the specific responsibility or contribution.",
    "did": "Use a precise action verb describing the actual work.",
    "made": "Use a more specific action such as developed, designed, created, or implemented.",
    "used": "Explain what you accomplished using the technology.",
}


ACTION_VERBS = {
    "developed", "designed", "implemented", "built", "created", "engineered",
    "automated", "analyzed", "optimized", "improved", "deployed", "integrated",
    "tested", "evaluated", "led", "managed", "configured", "trained", "architected", "refactored"
}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def find_weak_phrases(text: str) -> List[str]:
    normalized = normalize_text(text).lower()
    return [phrase for phrase in WEAK_PHRASES if phrase in normalized]


def find_action_verbs(text: str) -> List[str]:
    words = set(re.findall(r"\b[a-zA-Z]+\b", normalize_text(text).lower()))
    return sorted(verb for verb in ACTION_VERBS if verb in words)


def find_metrics(text: str) -> List[str]:
    patterns = [
        r"\b\d+(?:\.\d+)?\s*%",
        r"\b\d+(?:\.\d+)?\s*(?:years?|months?)\b",
        r"\b\d+(?:\.\d+)?\s*(?:users?|clients?|projects?)\b",
        r"\b\d+(?:\.\d+)?\s*(?:ms|seconds?|minutes?|hours?)\b",
        r"\$\s?\d+(?:,\d{3})*(?:\.\d+)?",
        r"\b\d+(?:,\d{3})+\b",
    ]
    matches = []
    for pattern in patterns:
        matches.extend(re.findall(pattern, text or "", flags=re.I))
    return sorted(set(matches))


def find_technical_terms(text: str) -> List[str]:
    technical_terms = {
        "python", "sql", "tensorflow", "pytorch", "scikit-learn", "opencv",
        "pandas", "numpy", "docker", "kubernetes", "aws", "azure", "gcp",
        "git", "github", "streamlit", "machine learning", "deep learning",
        "computer vision", "nlp", "natural language processing", "api", "rest",
        "postgresql", "mysql", "mongodb",
    }
    normalized = normalize_text(text).lower()
    return sorted(term for term in technical_terms if term in normalized)


def analyze_bullet(text: str) -> ImprovementResult:
    text = normalize_text(text)

    if not text:
        return ImprovementResult(
            original_text=text,
            suggestions=["Add a meaningful accomplishment or responsibility."],
            detected_issues=["Empty content"],
            score=0.0,
        )

    suggestions = []
    issues = []

    weak_phrases = find_weak_phrases(text)
    action_verbs = find_action_verbs(text)
    metrics = find_metrics(text)
    technical_terms = find_technical_terms(text)

    for phrase in weak_phrases:
        issues.append(f"Generic phrase detected: '{phrase}'")
        suggestions.append(WEAK_PHRASES[phrase])

    if not action_verbs:
        issues.append("No strong action verb detected.")
        suggestions.append("Start with a precise action verb such as developed, implemented, analyzed, designed, or optimized when truthful.")

    word_count = len(text.split())
    if word_count < 6:
        issues.append("Bullet is very short.")
        suggestions.append("Provide more context about what you did, which technology or method you used, and the outcome.")
    elif word_count < 12:
        issues.append("Bullet may lack useful detail.")
        suggestions.append("Consider adding the technology, method, or outcome if relevant.")

    if not metrics:
        issues.append("No measurable result detected.")
        suggestions.append("Add a measurable outcome if you have one. Do not invent metrics.")

    if not technical_terms:
        suggestions.append("Consider naming relevant technologies, tools, methods, or domain-specific techniques if applicable.")

    score = 100.0
    if weak_phrases:
        score -= min(25, len(weak_phrases) * 10)
    if not action_verbs:
        score -= 20
    if word_count < 12:
        score -= 15
    if not metrics:
        score -= 10
    if not technical_terms:
        score -= 10

    score = max(0.0, min(100.0, score))

    return ImprovementResult(
        original_text=text,
        suggestions=list(dict.fromkeys(suggestions)),
        detected_issues=list(dict.fromkeys(issues)),
        action_verbs_found=action_verbs,
        metrics_found=metrics,
        technical_terms_found=technical_terms,
        score=round(score, 2),
    )


def analyze_bullets(bullets: List[str]) -> dict:
    cleaned_bullets = [normalize_text(bullet) for bullet in bullets if normalize_text(bullet)]

    if not cleaned_bullets:
        return {
            "bullet_results": [],
            "overall_score": 0.0,
            "repeated_starters": [],
            "section_suggestions": ["Add at least one meaningful experience or project bullet."],
        }

    results = [analyze_bullet(bullet) for bullet in cleaned_bullets]

    starters = []
    for bullet in cleaned_bullets:
        words = bullet.lower().split()
        if words:
            starters.append(words[0])

    starter_counts = {}
    for starter in starters:
        starter_counts[starter] = starter_counts.get(starter, 0) + 1

    repeated_starters = sorted(starter for starter, count in starter_counts.items() if count >= 2)

    section_suggestions = []

    if repeated_starters:
        section_suggestions.append(f"Several bullets begin with the same word: {', '.join(repeated_starters)}. Consider varying action verbs where appropriate.")

    bullets_without_metrics = [result for result in results if not result.metrics_found]
    if bullets_without_metrics:
        section_suggestions.append("Some bullets do not contain measurable outcomes. Add metrics only when you have genuine results to report.")

    bullets_without_actions = [result for result in results if not result.action_verbs_found]
    if bullets_without_actions:
        section_suggestions.append("Some bullets lack strong action verbs. Use precise verbs that accurately describe your work.")

    technical_count = sum(bool(result.technical_terms_found) for result in results)
    if technical_count == 0:
        section_suggestions.append("Consider mentioning relevant technologies, tools, methods, or domain-specific techniques.")

    short_bullets = [result for result in results if len(result.original_text.split()) < 12]
    if short_bullets:
        section_suggestions.append("Some bullets are short and may benefit from additional context about the work performed and its outcome.")

    individual_scores = [result.score for result in results]
    overall_score = round(max(0.0, min(100.0, sum(individual_scores) / len(individual_scores))), 2)

    return {
        "bullet_results": results,
        "overall_score": overall_score,
        "repeated_starters": repeated_starters,
        "section_suggestions": list(dict.fromkeys(section_suggestions)),
    }


def analyze_summary(summary: str) -> dict:
    summary = normalize_text(summary)

    if not summary:
        return {
            "score": 0.0,
            "word_count": 0,
            "issues": ["Professional summary is missing."],
            "suggestions": ["Add a concise professional summary describing your role, expertise, and relevant strengths."],
            "action_verbs": [],
            "technical_terms": [],
            "generic_phrases": [],
        }

    words = summary.split()
    word_count = len(words)

    action_verbs = find_action_verbs(summary)
    technical_terms = find_technical_terms(summary)
    generic_phrases = find_weak_phrases(summary)

    issues = []
    suggestions = []

    if word_count < 20:
        issues.append("Summary is very short.")
        suggestions.append("Consider adding more relevant detail about your professional focus and technical strengths.")
    elif word_count > 100:
        issues.append("Summary may be too long.")
        suggestions.append("Consider reducing the summary to the most relevant professional information.")

    first_person_pattern = r"\b(i|i'm|i am|my|me|we|our)\b"
    first_person_words = re.findall(first_person_pattern, summary.lower())
    if first_person_words:
        issues.append("First-person language detected.")
        suggestions.append("Consider using concise professional phrasing without first-person pronouns.")

    if generic_phrases:
        issues.append("Generic or weak phrases detected.")
        for phrase in generic_phrases:
            suggestions.append(WEAK_PHRASES[phrase])

    professional_roles = {"engineer", "developer", "scientist", "analyst", "designer", "manager", "researcher", "specialist", "architect", "consultant", "student", "graduate"}
    normalized_summary = summary.lower()
    role_detected = any(role in normalized_summary for role in professional_roles)

    if not role_detected:
        issues.append("Clear professional role or identity not detected.")
        suggestions.append("Clearly state your professional role or target career direction when appropriate.")

    if not technical_terms:
        suggestions.append("Consider mentioning relevant technologies, tools, methods, or domain expertise.")

    if not action_verbs:
        suggestions.append("Consider describing meaningful areas of work, expertise, or contributions using precise language.")

    score = 100.0
    if word_count < 20:
        score -= 20
    elif word_count > 100:
        score -= 10
    if first_person_words:
        score -= 10
    if generic_phrases:
        score -= min(25, len(generic_phrases) * 10)
    if not role_detected:
        score -= 20
    if not technical_terms:
        score -= 10
    if not action_verbs:
        score -= 5

    score = max(0.0, min(100.0, score))

    return {
        "score": round(score, 2),
        "word_count": word_count,
        "issues": list(dict.fromkeys(issues)),
        "suggestions": list(dict.fromkeys(suggestions)),
        "action_verbs": action_verbs,
        "technical_terms": technical_terms,
        "generic_phrases": generic_phrases,
    }


def generate_improvement_report(
    summary: str = "",
    experience_bullets: List[str] | None = None,
    project_bullets: List[str] | None = None,
) -> dict:
    experience_bullets = experience_bullets or []
    project_bullets = project_bullets or []

    summary_result = analyze_summary(summary)
    experience_result = analyze_bullets(experience_bullets)
    project_result = analyze_bullets(project_bullets)

    section_scores = []
    section_weights = []

    if normalize_text(summary):
        section_scores.append(summary_result["score"])
        section_weights.append(30)

    if experience_bullets:
        section_scores.append(experience_result["overall_score"])
        section_weights.append(50)

    if project_bullets:
        section_scores.append(project_result["overall_score"])
        section_weights.append(20)

    if section_scores:
        total_weight = sum(section_weights)
        overall_score = sum(score * weight for score, weight in zip(section_scores, section_weights)) / total_weight
    else:
        overall_score = 0.0

    overall_score = round(max(0.0, min(100.0, overall_score)), 2)

    priority_issues = []
    priority_issues.extend(summary_result["issues"])
    for result in experience_result["bullet_results"]:
        priority_issues.extend(result.detected_issues)
    for result in project_result["bullet_results"]:
        priority_issues.extend(result.detected_issues)
    priority_issues = list(dict.fromkeys(priority_issues))

    recommendations = []
    recommendations.extend(summary_result["suggestions"])
    recommendations.extend(experience_result["section_suggestions"])
    recommendations.extend(project_result["section_suggestions"])
    recommendations = list(dict.fromkeys(recommendations))

    return {
        "overall_score": overall_score,
        "summary": summary_result,
        "experience": experience_result,
        "projects": project_result,
        "priority_issues": priority_issues,
        "recommendations": recommendations,
    }
