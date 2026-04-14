# Author: Vansh Gulati

import streamlit as st
import requests
import time

st.set_page_config(
    page_title="Vansh AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# ---------- RETRY FUNCTION ----------
def call_api_with_retry(url, files, data):
    for attempt in range(3):
        try:
            response = requests.post(
                url,
                files=files,
                data=data,
                timeout=60
            )
            return response
        except requests.exceptions.RequestException:
            time.sleep(5)
    return None

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
.big-title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: #AAAAAA;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<p class="big-title">AI Resume Analyzer</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Built by Vansh Gulati</p>', unsafe_allow_html=True)
st.write("---")

# ---------- INPUT SECTION ----------
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📄 Upload Resume")
    uploaded_file = st.file_uploader("", type=["pdf", "txt"])

with col2:
    st.markdown("### 📝 Job Description")
    job_description = st.text_area("", height=200)

st.write("")

# ---------- BUTTON ----------
analyze = st.button("🚀 Analyze Resume")

# ---------- LOGIC ----------
if analyze:
    if uploaded_file and job_description:

        with st.spinner("Analyzing your resume..."):

            response = call_api_with_retry(
                "https://ai-resume-analyzer.onrender.com/analyze",
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                },
                data={"job_description": job_description}
            )

        # 🔴 If backend sleeping / failed
        if response is None:
            st.error("⏳ Backend is starting (Render sleep). Please try again in 10 seconds.")
        
        else:
            st.write("Status Code:", response.status_code)  # Debug (remove later)

            if response.status_code == 200:
                result = response.json()

                st.write("---")

                # ---------- SCORE ----------
                score = result["match_score"]

                st.markdown("### 📊 Match Score")
                st.progress(int(score))
                st.success(f"{score}% Match")

                # ---------- SCORE BREAKDOWN ----------
                st.write("---")
                st.subheader("📈 Score Breakdown")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Semantic", result["semantic_score"])

                with col2:
                    st.metric("Skills", result["skills_score"])

                with col3:
                    st.metric("Experience", result["experience_score"])

                # ---------- DOMAIN ----------
                st.info(f"Detected Domain: {result['domain']}")

                # ---------- SKILLS ----------
                st.write("---")
                st.subheader("🧠 Skills Analysis")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### ✅ Matched Skills")
                    if result["matched_skills"]:
                        for skill in result["matched_skills"]:
                            st.success(skill)
                    else:
                        st.write("No matched skills")

                with col2:
                    st.markdown("#### ❌ Missing Skills")
                    if result["missing_skills"]:
                        for skill in result["missing_skills"]:
                            st.error(skill)
                    else:
                        st.write("No missing skills")

                # ---------- RECOMMENDATIONS ----------
                st.write("---")
                st.subheader("💡 Recommendations")

                if result["missing_skills"]:
                    st.warning("Add these skills to improve your resume:")
                    for skill in result["missing_skills"]:
                        st.write(f"- {skill}")
                else:
                    st.success("Excellent match! Your resume fits the job well.")

            else:
                st.error("Backend error occurred")
                st.write("Response:", response.text)

    else:
        st.warning("Please upload a resume and enter job description.")

# ---------- FOOTER ----------
st.write("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>Made with ❤️ by Vansh Gulati</p>",
    unsafe_allow_html=True
)