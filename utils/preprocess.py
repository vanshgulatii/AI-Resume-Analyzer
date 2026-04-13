# Author: Vansh Gulati

import re

# -------------------------------
# Skill Dictionaries (Multi-Domain)
# -------------------------------

TECH_SKILLS = [
    "python", "java", "c++", "c", "javascript", "typescript",
    "react", "angular", "vue", "node.js", "django", "flask",
    "spring boot", "html", "css",
    "machine learning", "deep learning", "data science",
    "nlp", "computer vision", "artificial intelligence",
    "tensorflow", "pytorch", "scikit-learn",
    "pandas", "numpy", "matplotlib",
    "sql", "mongodb", "postgresql",
    "docker", "kubernetes", "aws", "azure", "gcp",
    "git", "linux"
]

HR_SKILLS = [
    "recruitment", "talent acquisition", "onboarding",
    "employee relations", "payroll", "hr policies",
    "performance management", "training and development",
    "compensation and benefits", "workforce planning",
    "conflict resolution", "organizational development"
]

BUSINESS_SKILLS = [
    "project management", "stakeholder management",
    "leadership", "communication", "strategy",
    "operations", "business analysis",
    "problem solving", "decision making",
    "time management", "negotiation"
]

FINANCE_SKILLS = [
    "financial analysis", "accounting", "budgeting",
    "forecasting", "financial modeling",
    "excel", "risk management",
    "auditing", "taxation", "investment analysis"
]

MARKETING_SKILLS = [
    "digital marketing", "seo", "sem", "content marketing",
    "social media marketing", "branding",
    "market research", "campaign management",
    "email marketing", "google analytics"
]

# Combine all skills
ALL_SKILLS = list(set(
    TECH_SKILLS +
    HR_SKILLS +
    BUSINESS_SKILLS +
    FINANCE_SKILLS +
    MARKETING_SKILLS
))


# -------------------------------
# Text Cleaning
# -------------------------------

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s\+\#\.]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# -------------------------------
# Skill Extraction
# -------------------------------

def extract_skills(text):
    text = clean_text(text)
    found_skills = []

    for skill in ALL_SKILLS:
        # exact word or phrase match
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))


# -------------------------------
# Domain Detection
# -------------------------------

def detect_domain(skills):
    skills = set(skills)

    if skills & set(TECH_SKILLS):
        return "tech"
    elif skills & set(HR_SKILLS):
        return "hr"
    elif skills & set(FINANCE_SKILLS):
        return "finance"
    elif skills & set(MARKETING_SKILLS):
        return "marketing"
    else:
        return "general"