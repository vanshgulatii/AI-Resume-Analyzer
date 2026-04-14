# Author: Vansh Gulati

import io
import os
import requests
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import pdfplumber
from fastapi import FastAPI, UploadFile, File, Form
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.preprocess import extract_skills, detect_domain

app = FastAPI()

# 🔐 Get API key from environment (IMPORTANT)
HF_API_KEY = os.getenv("HF_API_KEY")


@app.get("/")
def home():
    return {"message": "AI Resume Analyzer API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


# 🔥 HuggingFace API similarity
def get_similarity_score_api(text, job_description):
    if not HF_API_KEY:
        return None

    API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    payload = {
        "inputs": {
            "source_sentence": text[:1000],
            "sentences": [job_description[:1000]]
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)

        if response.status_code == 200:
            return response.json()[0] * 100
        else:
            return None

    except Exception:
        return None


# 🔥 TF-IDF fallback (always works)
def get_similarity_score_tfidf(text, job_description):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text, job_description])

    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100


# Experience scoring
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

    elif file.filename.endswith(".txt"):
        text = content.decode("utf-8")

    else:
        return {"error": "Only PDF or TXT files allowed"}

    # 🔥 Try API first, fallback to TF-IDF
    similarity_score = get_similarity_score_api(text, job_description)

    if similarity_score is None:
        similarity_score = get_similarity_score_tfidf(text, job_description)

    # Skills
    resume_skills = extract_skills(text)
    job_skills = extract_skills(job_description)

    domain = detect_domain(resume_skills)

    matched_skills = list(set(resume_skills) & set(job_skills))
    missing_skills = list(set(job_skills) - set(resume_skills))

    skills_score = min(len(matched_skills) * 5, 30)

    # Experience
    experience_score = calculate_experience_score(text)

    # Final score
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