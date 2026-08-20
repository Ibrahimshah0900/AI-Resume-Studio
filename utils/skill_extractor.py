
from __future__ import annotations

import re
from collections import OrderedDict
from typing import Dict, List, Set

from utils.text_cleaner import clean_for_matching


SKILL_DATABASE = {
    "Programming Languages": {
        "Python": ["python"], "C++": ["c++", "cpp"], "C#": ["c#", "csharp"],
        "Java": ["java"], "JavaScript": ["javascript", "js"], "TypeScript": ["typescript", "ts"],
        "Go": ["golang", "go"], "R": ["r programming"], "PHP": ["php"], "Ruby": ["ruby"],
        "Swift": ["swift"], "Kotlin": ["kotlin"],
    },
    "Data Science": {
        "Pandas": ["pandas"], "NumPy": ["numpy"], "Matplotlib": ["matplotlib"],
        "Seaborn": ["seaborn"], "Jupyter": ["jupyter", "jupyter notebook"],
        "SciPy": ["scipy"], "Statsmodels": ["statsmodels"],
    },
    "Machine Learning": {
        "Scikit-learn": ["scikit-learn", "scikit learn", "sklearn"],
        "XGBoost": ["xgboost"], "LightGBM": ["lightgbm"], "CatBoost": ["catboost"],
        "Machine Learning": ["machine learning"],
    },
    "Deep Learning": {
        "TensorFlow": ["tensorflow"], "PyTorch": ["pytorch"], "Keras": ["keras"],
        "Transformers": ["transformers", "hugging face transformers"],
        "Deep Learning": ["deep learning"],
    },
    "Computer Vision": {
        "OpenCV": ["opencv", "opencv-python"], "YOLO": ["yolo", "yolov5", "yolov8"],
        "Computer Vision": ["computer vision"], "Image Processing": ["image processing"],
    },
    "Natural Language Processing": {
        "NLP": ["nlp", "natural language processing"], "spaCy": ["spacy"],
        "NLTK": ["nltk"], "Sentence Transformers": ["sentence transformers", "sentence-transformers"],
    },
    "Databases": {
        "SQL": ["sql"], "MySQL": ["mysql"], "PostgreSQL": ["postgresql", "postgres"],
        "SQLite": ["sqlite"], "MongoDB": ["mongodb", "mongo db"], "Redis": ["redis"],
    },
    "Cloud": {
        "AWS": ["aws", "amazon web services"], "Azure": ["azure", "microsoft azure"],
        "Google Cloud": ["google cloud", "gcp"], "Firebase": ["firebase"],
    },
    "DevOps": {
        "Git": ["git"], "GitHub": ["github"], "GitLab": ["gitlab"],
        "Docker": ["docker"], "Kubernetes": ["kubernetes", "k8s"],
        "CI/CD": ["ci/cd", "continuous integration"], "Linux": ["linux"],
    },
    "Backend": {
        "FastAPI": ["fastapi"], "Django": ["django"], "Flask": ["flask"],
        "REST API": ["rest api", "restful api"], "GraphQL": ["graphql"],
    },
    "Frontend": {
        "React": ["react", "reactjs"], "Angular": ["angular"], "Vue.js": ["vue", "vuejs"],
        "HTML": ["html", "html5"], "CSS": ["css", "css3"],
        "Tailwind CSS": ["tailwind", "tailwind css"],
    },
    "Tools": {
        "Streamlit": ["streamlit"], "VS Code": ["vs code", "visual studio code"],
        "Jira": ["jira"], "Postman": ["postman"], "Power BI": ["power bi"], "Tableau": ["tableau"],
    },
    "Soft Skills": {
        "Communication": ["communication"], "Leadership": ["leadership"],
        "Problem Solving": ["problem solving", "problem-solving"],
        "Teamwork": ["teamwork", "team work"], "Project Management": ["project management"],
    },
}


def _contains_skill(text: str, alias: str) -> bool:
    alias = alias.lower().strip()
    if not alias:
        return False
    if len(alias) <= 2:
        pattern = r"(?<![a-z0-9+#])" + re.escape(alias) + r"(?![a-z0-9+#])"
    else:
        pattern = r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def extract_skills(text: str) -> Dict[str, List[str]]:
    cleaned = clean_for_matching(text)
    if not cleaned:
        return {}

    detected = OrderedDict()
    for category, skills in SKILL_DATABASE.items():
        category_skills = []
        for canonical_name, aliases in skills.items():
            for alias in aliases:
                if _contains_skill(cleaned, alias):
                    if canonical_name not in category_skills:
                        category_skills.append(canonical_name)
                    break
        if category_skills:
            detected[category] = category_skills

    return dict(detected)


def extract_flat_skills(text: str) -> List[str]:
    grouped = extract_skills(text)
    skills = []
    for category_skills in grouped.values():
        for skill in category_skills:
            if skill not in skills:
                skills.append(skill)
    return skills


def extract_skill_categories(text: str) -> Dict[str, int]:
    grouped = extract_skills(text)
    return {category: len(skills) for category, skills in grouped.items()}


def compare_skills(resume_text: str, job_text: str) -> Dict[str, List[str]]:
    resume_skills = set(extract_flat_skills(resume_text))
    job_skills = set(extract_flat_skills(job_text))
    return {
        "matching": sorted(resume_skills & job_skills),
        "missing": sorted(job_skills - resume_skills),
        "additional": sorted(resume_skills - job_skills),
    }
