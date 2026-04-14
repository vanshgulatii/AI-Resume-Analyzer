# Author: Vansh Gulati

import streamlit as st
import requests

st.set_page_config(
    page_title="Vansh AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# CUSTOM CSS
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
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #1E1E1E;
    box-shadow: 0px 0px 15px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<p class="big-title">AI Resume Analyzer</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Built by Vansh Gulati</p>', unsafe_allow_html=True)
st.write("---")

#  INPUT SECTION
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📄 Upload Resume")
    uploaded_file = st.file_uploader("", type=["pdf", "txt"])

with col2:
    st.markdown("### 📝 Job Description")
    job_description = st.text_area("", height=200)

st.write("")

# BUTTON 
analyze = st.button("🚀 Analyze Resume")

# LOGIC
if analyze:
    if uploaded_file and job_description:

        with st.spinner("Analyzing your resume..."):

            response = requests.post(
                ""https://ai-resume-analyzer.onrender.com/analyze"",
                files={"file": (uploaded_file.name, uploaded_file.getvalue())},
                data={"job_description": job_description}
            )

        if response.status_code == 200:
            result = response.json()

            st.write("---")

            # SCORE
            score = result["match_score"]

            st.markdown("### 📊 Match Score")
            st.progress(int(score))
            st.success(f"{score}% Match")

            # DOMAIN 
            st.info(f"Detected Domain: {result['domain']}")

            # SKILLS 
            st.markdown("### 🧠 Skills Analysis")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### ✅ Matched Skills")
                if result["matched_skills"]:
                    for skill in result["matched_skills"]:
                        st.markdown(f"- {skill}")
                else:
                    st.write("No matched skills found")

            with col2:
                st.markdown("#### ❌ Missing Skills")
                if result["missing_skills"]:
                    for skill in result["missing_skills"]:
                        st.markdown(f"- {skill}")
                else:
                    st.write("No missing skills")

        else:
            st.error("Backend error. Please check if server is running.")

    else:
        st.warning("Please upload a resume and enter job description.")

# FOOTER
st.write("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>Made with ❤️ by Vansh Gulati</p>",
    unsafe_allow_html=True
)