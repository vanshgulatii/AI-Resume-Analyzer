# 🚀 AI Resume Analyzer API

An intelligent AI-powered API that analyzes resumes and matches them with job descriptions using Machine Learning.

🌍 Live Demo: https://ai-resume-analyzer-bdcq.onrender.com/docs

---

## 🔥 Features

- Upload Resume (PDF/TXT)
- Extract Skills from Resume
- Predict Resume Match Score using ML
- Compare Resume with Job Description
- Identify Missing Skills
- Fast API built with FastAPI

---

## 🛠 Tech Stack

- Python
- FastAPI
- Scikit-learn
- Pandas
- pdfplumber
- Uvicorn

---

## 🧠 How It Works

1. Upload resume (PDF/TXT)
2. Extract text from file
3. Detect skills using keyword matching
4. Convert text using TF-IDF
5. Predict score using ML model
6. Compare with job description
7. Identify missing skills

---

## 📂 Project Structure

ai-resume-analyzer/
│
├── app.py
├── train_model.py
├── requirements.txt
├── runtime.txt
│
├── model/
│   ├── model.pkl
│   └── vectorizer.pkl
│
└── utils/
    └── preprocess.py

---

## ▶️ Run Locally

git clone https://github.com/vanshgulatii/AI-Resume-Analyzer.git  
cd AI-Resume-Analyzer  

python3 -m venv venv  
source venv/bin/activate  

pip install -r requirements.txt  

python -m uvicorn app:app --reload  

Open: http://127.0.0.1:8000/docs

---

## 📌 API Endpoint

POST /analyze

### Inputs:
- Resume file (PDF/TXT)
- Job description (text)

### Output:
- Match score
- Resume skills
- Job skills
- Missing skills

---

## 🧪 Example Response

{
  "match_score": 88.5,
  "resume_skills": ["python", "pandas"],
  "job_skills": ["python", "machine learning", "sql"],
  "missing_skills": ["machine learning", "sql"],
  "status": "success"
}

---

## 💼 Use Case

- Helps job seekers improve resumes
- Identifies skill gaps
- Useful for ATS-like systems

---

## 🚀 Future Improvements

- Add frontend (React)
- Improve ML model accuracy
- Add advanced NLP features
- Docker deployment

---

## 👨‍💻 Author

Vansh Gulati  
GitHub: https://github.com/vanshgulatii  
LinkedIn: https://www.linkedin.com/in/vansh-g-31a607197/

---

⭐ If you like this project, give it a star!