# Author: Vansh Gulati

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils.preprocess import extract_skills

model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_score(resume, job_description):
    resume_emb = model.encode([resume])
    jd_emb = model.encode([job_description])

    similarity_score = cosine_similarity(resume_emb, jd_emb)[0][0] * 100

    resume_skills = extract_skills(resume)
    job_skills = extract_skills(job_description)

    matched_skills = list(set(resume_skills) & set(job_skills))
    skills_score = min(len(matched_skills) * 5, 30)

    final_score = similarity_score * 0.7 + skills_score * 0.3

    return final_score


test_data = [
    {
        "resume": "python machine learning data science pandas numpy",
        "job_description": "python data scientist machine learning",
        "expected_score": 85
    },
    {
        "resume": "deep learning pytorch computer vision ai",
        "job_description": "ai engineer deep learning computer vision",
        "expected_score": 90
    },
    {
        "resume": "sql data analysis excel dashboard",
        "job_description": "data analyst sql excel reporting",
        "expected_score": 80
    },
    {
        "resume": "html css javascript react frontend",
        "job_description": "frontend developer react js",
        "expected_score": 80
    },
    {
        "resume": "java spring boot backend microservices",
        "job_description": "backend developer java spring boot",
        "expected_score": 78
    },
    {
        "resume": "docker kubernetes aws cloud deployment",
        "job_description": "devops engineer aws docker kubernetes",
        "expected_score": 85
    },
    {
        "resume": "recruitment onboarding employee relations hr policies",
        "job_description": "hr specialist talent acquisition onboarding",
        "expected_score": 75
    },
    {
        "resume": "talent acquisition hiring employee engagement",
        "job_description": "human resource manager recruitment onboarding",
        "expected_score": 72
    },
    {
        "resume": "project management leadership communication strategy",
        "job_description": "business analyst stakeholder management strategy",
        "expected_score": 70
    },
    {
        "resume": "financial analysis budgeting forecasting excel",
        "job_description": "finance analyst accounting forecasting",
        "expected_score": 70
    },
    {
        "resume": "accounting auditing taxation financial reporting",
        "job_description": "chartered accountant financial reporting auditing",
        "expected_score": 75
    },
    {
        "resume": "digital marketing seo sem content marketing",
        "job_description": "marketing specialist seo content strategy",
        "expected_score": 78
    },
    {
        "resume": "social media marketing branding campaign management",
        "job_description": "marketing manager branding campaigns social media",
        "expected_score": 76
    },
    {
        "resume": "mechanical engineering thermodynamics fluid mechanics",
        "job_description": "software engineer python machine learning",
        "expected_score": 30
    },
    {
        "resume": "civil engineering construction project planning",
        "job_description": "data analyst python sql",
        "expected_score": 25
    }
]


errors = []

for sample in test_data:
    predicted = calculate_score(sample["resume"], sample["job_description"])
    expected = sample["expected_score"]

    error = abs(predicted - expected)
    errors.append(error)

    print(f"Predicted: {round(predicted, 2)}, Expected: {expected}, Error: {round(error, 2)}")

average_error = sum(errors) / len(errors)

print("\nAverage Error:", round(average_error, 2))