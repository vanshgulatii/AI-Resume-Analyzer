SKILLS = [
    "python", "machine learning", "data science",
    "deep learning", "pytorch", "tensorflow",
    "sql", "pandas", "numpy", "java",
    "javascript", "react", "html", "css"
]

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))