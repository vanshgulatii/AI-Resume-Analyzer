# Author: Vansh Gulati

import streamlit as st
import requests

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("AI Resume Analyzer")
st.write("Upload your resume and compare it with a job description")

uploaded_file = st.file_uploader("Upload Resume (PDF/TXT)", type=["pdf", "txt"])
job_description = st.text_area("Enter Job Description")

if st.button("Analyze"):
    if uploaded_file and job_description:
        files = {"file": uploaded_file.getvalue()}
        data = {"job_description": job_description}

        response = requests.post(
            "http://127.0.0.1:8000/analyze",
            files={"file": uploaded_file},
            data=data
        )

        if response.status_code == 200:
            result = response.json()

            st.subheader("Results")
            st.write(f"Match Score: {result['match_score']}%")
            st.write(f"Domain: {result['domain']}")

            st.subheader("Skills")
            st.write("Matched Skills:", result["matched_skills"])
            st.write("Missing Skills:", result["missing_skills"])
        else:
            st.error("Error analyzing resume")
    else:
        st.warning("Please upload a file and enter job description")