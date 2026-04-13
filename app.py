import io
import pdfplumber
from fastapi import FastAPI, UploadFile, File, Form
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils.preprocess import extract_skills

app = FastAPI()

# Load BERT model 
bert_model = SentenceTransformer('all-MiniLM-L6-v2')


@app.get("/")
def home():
    return {"message": "AI Resume Analyzer API (BERT Version) is running 🚀"}


# Experience scoring function
def calculate_experience_score(text):
    keywords = ["experience", "worked", "intern", "project", "developer"]
    score = sum([text.lower().count(k) for k in keywords])
    return min(score * 2, 20)  # max 20 points


@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    content = await file.read()
    text = ""

    #  PDF handling
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

    #  TXT handling
    elif file.filename.endswith(".txt"):
        text = content.decode("utf-8")

    else:
        return {"error": "Only PDF or TXT files allowed"}

    # BERT-based semantic similarity
    resume_embedding = bert_model.encode([text])
    jd_embedding = bert_model.encode([job_description])

    similarity_score = cosine_similarity(resume_embedding, jd_embedding)[0][0] * 100

    # Skill extraction
    resume_skills = extract_skills(text)
    job_skills = extract_skills(job_description)

    #  Skill matching score
    matched_skills = list(set(resume_skills) & set(job_skills))
    missing_skills = list(set(job_skills) - set(resume_skills))

    skills_score = min(len(matched_skills) * 5, 30)  # max 30

    #  Experience score
    experience_score = calculate_experience_score(text)

    # Final combined score
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
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "missing_skills": missing_skills,
        "status": "success"
    }