import pdfplumber
import io
from utils.preprocess import extract_skills
from fastapi import FastAPI, UploadFile, File
from fastapi import Form
import pickle

app = FastAPI()

# load model
model = pickle.load(open("model/model.pkl", "rb"))
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))

@app.get("/")
def home():
    return {"message": "AI Resume Analyzer API is running 🚀"}


@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    content = await file.read()

    text = ""

    # PDF handling
    if file.filename.endswith(".pdf"):
        import pdfplumber, io
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

    # TXT handling
    elif file.filename.endswith(".txt"):
        text = content.decode("utf-8")

    else:
        return {"error": "Only PDF or TXT files allowed"}

    # ML prediction
    processed = vectorizer.transform([text])
    score = model.predict(processed)[0]

    # Extract skills
    resume_skills = extract_skills(text)
    job_skills = extract_skills(job_description)

    # 🔥 Missing skills
    missing_skills = list(set(job_skills) - set(resume_skills))

    return {
        "match_score": round(float(score), 2),
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "missing_skills": missing_skills,
        "status": "success"
    }