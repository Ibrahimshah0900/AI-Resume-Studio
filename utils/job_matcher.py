
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class JobMatchResult:
    tfidf_similarity: float = 0.0
    semantic_similarity: Optional[float] = None
    skill_match_score: float = 0.0
    final_match_score: float = 0.0
    matching_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    additional_resume_skills: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


def _normalize_skill(skill: str) -> str:
    return " ".join(str(skill).strip().lower().split())


def calculate_tfidf_similarity(resume_text: str, job_description: str) -> float:
    resume_text = str(resume_text or "").strip()
    job_description = str(job_description or "").strip()

    if not resume_text or not job_description:
        return 0.0

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
    )

    try:
        matrix = vectorizer.fit_transform([resume_text, job_description])
    except ValueError:
        return 0.0

    similarity = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    return round(float(similarity) * 100, 2)


def calculate_semantic_similarity(resume_text: str, job_description: str, model) -> float:
    resume_text = str(resume_text or "").strip()
    job_description = str(job_description or "").strip()

    if not resume_text or not job_description:
        return 0.0

    embeddings = model.encode(
        [resume_text, job_description],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    similarity = float(cosine_similarity(embeddings[0:1], embeddings[1:2])[0][0])
    similarity = max(0.0, min(1.0, similarity))
    return round(similarity * 100, 2)


def compare_skills(resume_skills: List[str], job_skills: List[str]) -> Dict[str, List[str] | float]:
    resume_map = {_normalize_skill(skill): str(skill).strip() for skill in (resume_skills or []) if str(skill).strip()}
    job_map = {_normalize_skill(skill): str(skill).strip() for skill in (job_skills or []) if str(skill).strip()}

    resume_set = set(resume_map)
    job_set = set(job_map)

    matching = sorted(resume_map[key] for key in resume_set.intersection(job_set))
    missing = sorted(job_map[key] for key in job_set.difference(resume_set))
    additional = sorted(resume_map[key] for key in resume_set.difference(job_set))

    skill_score = (len(resume_set.intersection(job_set)) / len(job_set) * 100) if job_set else 0.0

    return {
        "matching_skills": matching,
        "missing_skills": missing,
        "additional_resume_skills": additional,
        "skill_match_score": round(skill_score, 2),
    }


def generate_recommendations(
    tfidf_similarity: float,
    skill_match_score: float,
    missing_skills: List[str],
    semantic_similarity: Optional[float] = None,
) -> List[str]:
    recommendations = []

    if tfidf_similarity < 40:
        recommendations.append("The resume has relatively low textual similarity to this job description. Review the role requirements and tailor relevant experience where truthful.")
    elif tfidf_similarity < 65:
        recommendations.append("Consider tailoring relevant resume wording to better reflect the terminology used in the job description.")

    if skill_match_score < 50:
        recommendations.append("Several important job skills are not currently detected in the resume.")
    elif skill_match_score < 75:
        recommendations.append("Review the missing job skills and include only those you genuinely possess.")

    if missing_skills:
        recommendations.append("Do not add missing skills unless you actually have the corresponding knowledge or experience.")

    if semantic_similarity is not None and semantic_similarity >= 75 and tfidf_similarity < 50:
        recommendations.append("The resume appears semantically relevant even though keyword overlap is relatively low. Consider using clearer terminology from the job description where it truthfully reflects your experience.")

    if not recommendations:
        recommendations.append("The resume shows strong alignment with the provided job description. Continue verifying that the experience and skills accurately represent your background.")

    return recommendations


def match_resume_to_job(
    resume_text: str,
    job_description: str,
    resume_skills: List[str],
    job_skills: List[str],
    tfidf_weight: float = 0.60,
    skill_weight: float = 0.40,
) -> JobMatchResult:
    if tfidf_weight < 0 or skill_weight < 0:
        raise ValueError("Weights must be non-negative.")
    total_weight = tfidf_weight + skill_weight
    if total_weight <= 0:
        raise ValueError("At least one matching weight must be positive.")

    tfidf_weight /= total_weight
    skill_weight /= total_weight

    tfidf_score = calculate_tfidf_similarity(resume_text, job_description)
    skill_result = compare_skills(resume_skills, job_skills)
    skill_score = float(skill_result["skill_match_score"])

    final_score = tfidf_score * tfidf_weight + skill_score * skill_weight

    recommendations = generate_recommendations(tfidf_score, skill_score, skill_result["missing_skills"])

    return JobMatchResult(
        tfidf_similarity=round(tfidf_score, 2),
        skill_match_score=round(skill_score, 2),
        final_match_score=round(final_score, 2),
        matching_skills=skill_result["matching_skills"],
        missing_skills=skill_result["missing_skills"],
        additional_resume_skills=skill_result["additional_resume_skills"],
        recommendations=recommendations,
    )


def match_resume_to_job_semantic(
    resume_text: str,
    job_description: str,
    resume_skills: List[str],
    job_skills: List[str],
    model,
    tfidf_weight: float = 0.35,
    semantic_weight: float = 0.35,
    skill_weight: float = 0.30,
) -> JobMatchResult:
    weights = [tfidf_weight, semantic_weight, skill_weight]
    if any(w < 0 for w in weights):
        raise ValueError("Weights must be non-negative.")
    total_weight = sum(weights)
    if total_weight <= 0:
        raise ValueError("At least one matching weight must be positive.")

    tfidf_weight /= total_weight
    semantic_weight /= total_weight
    skill_weight /= total_weight

    tfidf_score = calculate_tfidf_similarity(resume_text, job_description)
    semantic_score = calculate_semantic_similarity(resume_text, job_description, model)
    skill_result = compare_skills(resume_skills, job_skills)
    skill_score = float(skill_result["skill_match_score"])

    final_score = tfidf_score * tfidf_weight + semantic_score * semantic_weight + skill_score * skill_weight

    recommendations = generate_recommendations(tfidf_score, skill_score, skill_result["missing_skills"], semantic_score)

    return JobMatchResult(
        tfidf_similarity=round(tfidf_score, 2),
        semantic_similarity=round(semantic_score, 2),
        skill_match_score=round(skill_score, 2),
        final_match_score=round(final_score, 2),
        matching_skills=skill_result["matching_skills"],
        missing_skills=skill_result["missing_skills"],
        additional_resume_skills=skill_result["additional_resume_skills"],
        recommendations=recommendations,
    )
