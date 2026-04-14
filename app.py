# Author: Vansh Gulati

import io
import pdfplumber
from fastapi import FastAPI, UploadFile, File, Form
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils.preprocess import extract_skills, detect_domain
import os

app = FastAPI()

bert_model = SentenceTransformer("all-MiniLM-L6-v2")


@app.get("/")
def home():
    return {"message": "AI Resume Analyzer API is running"}


@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    content = await file.read()
    text = ""

    if file.filename.endswith(".pdf"):
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

    elif file.filename.endswith(".txt"):
        text = content.decode("utf-8")

    else:
        return {"error": "Only PDF or TXT files allowed"}

    resume_embedding = bert_model.encode([text])
    jd_embedding = bert_model.encode([job_description])

    similarity_score = cosine_similarity(resume_embedding, jd_embedding)[0][0] * 100

    resume_skills = extract_skills(text)
    job_skills = extract_skills(job_description)

    domain = detect_domain(resume_skills)

    matched_skills = list(set(resume_skills) & set(job_skills))
    missing_skills = list(set(job_skills) - set(resume_skills))

    skills_score = min(len(matched_skills) * 5, 30)

    final_score = similarity_score * 0.7 + skills_score * 0.3
    final_score = max(0, min(final_score, 100))

    return {
        "match_score": round(float(final_score), 2),
        "semantic_score": round(float(similarity_score), 2),
        "skills_score": skills_score,
        "domain": domain,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "status": "success"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)