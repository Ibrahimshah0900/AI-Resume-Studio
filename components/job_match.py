
from __future__ import annotations
import streamlit as st
import re
from utils.job_matcher import match_resume_to_job
from utils.resume_text import resume_to_text
from utils.skill_extractor import extract_flat_skills
from utils.data_models import Resume
from utils.resume_builder_core import add_skill

def render_job_match() -> None:
    st.markdown('<div class="section-title">🎯 Job Match</div>', unsafe_allow_html=True)
    st.write("Compare your resume against a target job description using textual similarity and skill alignment.")

    resume = st.session_state.resume_data
    resume_text = resume_to_text(resume)
    resume_skills = extract_flat_skills(resume_text)

    job_description = st.text_area(
        "Target Job Description",
        value=st.session_state.get("job_match_description", ""),
        placeholder="Paste the complete target job description here...",
        height=250,
        key="job_match_job_description",
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🎯 Run Job Match", type="primary", use_container_width=True):
            if not resume_text.strip():
                st.warning("Your resume is currently empty. Complete your Resume Builder information first.")
                st.session_state.pop("job_match_result", None)
            elif not job_description.strip():
                st.warning("Please paste a target job description first.")
                st.session_state.pop("job_match_result", None)
            else:
                job_skills = extract_flat_skills(job_description)
                try:
                    result = match_resume_to_job(
                        resume_text=resume_text,
                        job_description=job_description,
                        resume_skills=resume_skills,
                        job_skills=job_skills,
                    )
                    st.session_state.job_match_result = result
                    st.session_state.job_match_description = job_description
                    st.success("Job match analysis completed.")
                except Exception as exc:
                    st.error(f"Job match analysis failed: {exc}")

    result = st.session_state.get("job_match_result")
    if not result:
        return

    st.divider()
    
    # Overall Score
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Final Match Score", f"{result.final_match_score:.1f} / 100", delta="", delta_color="normal")
    with col2:
        st.metric("TF-IDF Similarity", f"{result.tfidf_similarity:.1f}%")
    with col3:
        st.metric("Skill Match", f"{result.skill_match_score:.1f}%")

    st.subheader("Skills Analysis")
    
    # Display matching, missing, and additional skills with "Click to Add" functionality
    if result.matching_skills:
        st.success("**Matching skills:** " + ", ".join(result.matching_skills))
    
    if result.missing_skills:
        st.warning("**Missing skills:**")
        for skill in result.missing_skills:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"• {skill}")
            with col2:
                if st.button(f"➕ Add", key=f"add_missing_{skill}"):
                    add_skill(st.session_state.resume_data, skill)
                    st.success(f"Added {skill} to your resume!")
                    st.rerun()
    
    if result.additional_resume_skills:
        st.info("**Additional skills in resume:** " + ", ".join(result.additional_resume_skills))

    # Highlight missing keywords in job description
    if result.missing_skills:
        st.subheader("Job Description with Highlighted Missing Skills")
        highlighted_desc = job_description
        for skill in result.missing_skills:
            highlighted_desc = re.sub(
                r'\b' + re.escape(skill) + r'\b',
                f'<mark style="background-color: #ff6b6b; color: white; padding: 2px 4px; border-radius: 4px;">{skill}</mark>',
                highlighted_desc,
                flags=re.IGNORECASE
            )
        st.markdown(highlighted_desc, unsafe_allow_html=True)

    st.subheader("Recommendations")
    for recommendation in result.recommendations:
        st.info(f"→ {recommendation}")
