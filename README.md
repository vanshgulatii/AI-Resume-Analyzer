# 🚀 AI Resume Analyzer

An AI-powered full-stack web application that analyzes resumes against job descriptions using NLP techniques.  
It provides match scores, skill gap analysis, and improvement recommendations to help candidates optimize their resumes.

---

## 🌍 Live Demo

Frontend (Streamlit): https://ai-resume-analyzer-vansh-gulati.streamlit.app/  
Backend (FastAPI): https://ai-resume-analyzer-6ojk.onrender.com/docs  

---

## 🔥 Features

- Upload Resume (PDF/TXT)
- AI-based Resume vs Job Description Matching
- Match Score Calculation
- Skill Gap Analysis (Matched vs Missing Skills)
- Score Breakdown:
  - Semantic Score
  - Skills Score
  - Experience Score
- Resume Improvement Recommendations
- Download Analysis Report
- Lightweight and fast (optimized for deployment)

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- Scikit-learn (TF-IDF + Cosine Similarity)
- PDFPlumber

### Frontend
- Streamlit

### Deployment
- Render (Backend)
- Streamlit Cloud (Frontend)

---

## ⚙️ How It Works

1. Upload a resume (PDF/TXT)
2. Enter a job description
3. System processes:
   - Extracts text from resume
   - Computes semantic similarity (TF-IDF)
   - Extracts skills
   - Calculates match score
4. Displays:
   - Match score
   - Skills analysis
   - Recommendations

---

## 📊 Scoring Logic

Final Score is calculated as:

- 60% Semantic Similarity
- 25% Skills Match
- 15% Experience Score

---

## 🚀 How to Run Locally

### 1. Clone Repository

git clone https://github.com/vanshgulatii/AI-Resume-Analyzer.git  
cd AI-Resume-Analyzer  

---

### 2. Create Virtual Environment

python -m venv venv  
source venv/bin/activate  

---

### 3. Install Dependencies

pip install -r requirements.txt  

---

### 4. Run Backend

uvicorn app:app --reload  

---

### 5. Run Frontend

streamlit run streamlit_app.py  

---

## 🌐 Deployment

### Backend (Render)

Start command:

uvicorn app:app --host 0.0.0.0 --port $PORT  

---

### Frontend (Streamlit Cloud)

- Connected GitHub repository  
- Auto-deploy on push  

---

## ⚠️ Challenges Faced & Solutions

### 1. Render Port Binding Issue

Problem:  
No open ports detected  

Solution:  
Used dynamic port:

port = int(os.environ.get("PORT", 8000))

---

### 2. Heavy ML Model Crash

Problem:  
Sentence Transformers too heavy for free tier  

Solution:  
Replaced with TF-IDF (lightweight and fast)

---

### 3. Backend Sleep Issue (Render Free Tier)

Problem:  
Server sleeps → first request fails  

Solution:  
Added retry logic in frontend  

Expected behavior:  
First click may delay  
Second click works  

---

### 4. 404 Not Found Error

Problem:  
Wrong backend URL used  

Solution:  
Used correct endpoint:

https://ai-resume-analyzer-6ojk.onrender.com/analyze  

---

### 5. File Upload Issue

Problem:  
Incorrect file format in API request  

Solution:

files={"file": (uploaded_file.name, uploaded_file.getvalue())}

---

### 6. Missing Dependency

Problem:  
python-multipart not installed  

Solution:

pip install python-multipart  

---

## 🧠 Development Note

This project was primarily developed from a **Machine Learning Engineer perspective**.

- The core focus was on **NLP, scoring logic, and backend system design**
- Frontend (Streamlit) was implemented with the help of:
  - Guidance from peers
  - Documentation and community resources
  - LLM tools for faster UI iteration and debugging


---

##  Future Improvements

- GPT-based resume suggestions  
- Charts and visual analytics  
- PDF report generation  
- German language support  
- Recruiter dashboard  

---

##  Author

Vansh Gulati  
AI | Machine Learning 

---

## ⭐ If you like this project

Give it a star on GitHub ⭐