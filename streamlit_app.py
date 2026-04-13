# Author: Vansh Gulati

import streamlit as st
import requests

st.set_page_config(
    page_title="Vansh AI Resume Analyzer",
    page_icon="🚀",
    layout="centered"
)

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align: center;'>AI Resume Analyzer</h1>
    <h4 style='text-align: center;'>by Vansh Gulati</h4>
    <hr>
    """,
    unsafe_allow_html=True
)

st.write("Upload your resume and compare it with a job description")

# ---------------- INPUT ----------------
uploaded_file = st.file_uploader("Upload Resume (PDF/TXT)", type=["pdf", "txt"])
job_description = st.text_area("Enter Job Description")

# ---------------- BUTTON ----------------
if st.button("Analyze Resume"):
    if uploaded_file and job_description:

        with st.spinner("Analyzing resume..."):

            response = requests.post(
                "http://127.0.0.1:8000/analyze",
                files={
                    "file": (uploaded_file.name, uploaded_file.getvalue())
                },
                data={"job_description": job_description}
            )

        if response.status_code == 200:
            result = response.json()

            # ---------------- RESULTS ----------------
            st.success("Analysis Complete")

            # Score
            st.metric("Match Score", f"{result['match_score']}%")

            # Domain
            st.write(f"**Detected Domain:** {result['domain']}")

            # Skills
            st.subheader("Skills Analysis")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Matched Skills**")
                st.write(result["matched_skills"])

            with col2:
                st.write("**Missing Skills**")
                st.write(result["missing_skills"])

        else:
            st.error("Error analyzing resume")

    else:
        st.warning("Please upload a resume and enter job description")

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <p style='text-align: center;'>Built by Vansh Gulati | AI & Machine Learning</p>
    """,
    unsafe_allow_html=True
)