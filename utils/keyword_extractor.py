
from __future__ import annotations

import re
from typing import Dict, List, Set

from sklearn.feature_extraction.text import TfidfVectorizer
from utils.text_cleaner import clean_for_matching


GENERIC_KEYWORDS: Set[str] = {
    "using", "use", "used", "experience", "experienced", "candidate",
    "seeking", "strong", "preferred", "responsible", "responsibilities",
    "developed", "develop", "working", "worked", "work", "built", "build",
    "including", "include", "ability", "abilities", "knowledge", "skills",
    "skill", "professional", "professionals", "years", "year", "team", "teams",
}


def normalize_keyword(keyword: str) -> str:
    keyword = keyword.lower().strip()
    keyword = re.sub(r"\s+", " ", keyword)
    return keyword


def is_meaningful_keyword(keyword: str) -> bool:
    keyword = normalize_keyword(keyword)
    if not keyword:
        return False
    words = keyword.split()
    if len(words) == 1:
        if words[0] in GENERIC_KEYWORDS:
            return False
    if len(words) > 1:
        if words[0] in GENERIC_KEYWORDS:
            return False
        if words[-1] in GENERIC_KEYWORDS:
            return False
    if not re.search(r"[a-zA-Z]", keyword):
        return False
    return True


def extract_keywords(
    text: str,
    top_n: int = 20,
    ngram_range: tuple[int, int] = (1, 2),
    min_df: int = 1,
) -> List[Dict[str, float]]:
    if not isinstance(text, str):
        raise TypeError("text must be a string.")
    if top_n <= 0:
        raise ValueError("top_n must be greater than 0.")

    cleaned = clean_for_matching(text)
    if not cleaned:
        return []

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=ngram_range,
        min_df=min_df,
        token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z0-9+#.-]*\b",
    )

    try:
        matrix = vectorizer.fit_transform([cleaned])
    except ValueError:
        return []

    feature_names = vectorizer.get_feature_names_out()
    scores = matrix.toarray()[0]
    ranked_indices = scores.argsort()[::-1]

    results = []
    seen = set()

    for index in ranked_indices:
        score = float(scores[index])
        if score <= 0:
            continue
        keyword = normalize_keyword(feature_names[index])
        if not is_meaningful_keyword(keyword):
            continue
        if keyword in seen:
            continue
        seen.add(keyword)
        results.append({"keyword": keyword, "score": round(score, 6)})
        if len(results) >= top_n:
            break

    return results


def extract_keyword_list(text: str, top_n: int = 20, ngram_range: tuple[int, int] = (1, 2)) -> List[str]:
    return [item["keyword"] for item in extract_keywords(text=text, top_n=top_n, ngram_range=ngram_range)]


def compare_keywords(resume_text: str, job_text: str, top_n: int = 30) -> Dict[str, List[str]]:
    resume_keywords = set(extract_keyword_list(resume_text, top_n=top_n))
    job_keywords = set(extract_keyword_list(job_text, top_n=top_n))
    return {
        "matching": sorted(resume_keywords & job_keywords),
        "missing": sorted(job_keywords - resume_keywords),
        "additional": sorted(resume_keywords - job_keywords),
    }


def keyword_scores(text: str, top_n: int = 20) -> Dict[str, float]:
    return {item["keyword"]: item["score"] for item in extract_keywords(text, top_n=top_n)}
