# Author: Vansh Gulati

import io
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import pdfplumber
from fastapi import FastAPI, UploadFile, File, Form
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.preprocess import extract_skills, detect_domain

app = FastAPI()


@app.get("/")
def home():
    return {"message": "AI Resume Analyzer API is running"}


# Health check (important for Render)
@app.get("/health")
def health():
    return {"status": "ok"}


# Experience scoring function
def calculate_experience_score(text):
    keywords = ["experience", "intern", "project", "developed", "worked", "managed"]
    score = sum(text.lower().count(k) for k in keywords)
    return min(score * 2, 20)


@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    content = await file.read()
    text = ""

    # PDF handling
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

    # TXT handling
    elif file.filename.endswith(".txt"):
        text = content.decode("utf-8")

    else:
        return {"error": "Only PDF or TXT files allowed"}

    # 🔥 TF-IDF Semantic Similarity (LIGHT + EFFECTIVE)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text, job_description])

    similarity_score = (
        cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100
    )

    # Skill extraction
    resume_skills = extract_skills(text)
    job_skills = extract_skills(job_description)

    domain = detect_domain(resume_skills)

    matched_skills = list(set(resume_skills) & set(job_skills))
    missing_skills = list(set(job_skills) - set(resume_skills))

    skills_score = min(len(matched_skills) * 5, 30)

    # Experience score
    experience_score = calculate_experience_score(text)

    # Final score (balanced)
    final_score = (
        similarity_score * 0.6 +
        skills_score * 0.25 +
        experience_score * 0.15
    )

    final_score = max(0, min(final_score, 100))

    return {
        "match_score": round(float(final_score), 2),
        "semantic_score": round(float(similarity_score), 2),
        "skills_score": skills_score,
        "experience_score": experience_score,
        "domain": domain,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "status": "success"
    }


# Render-compatible startup
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)