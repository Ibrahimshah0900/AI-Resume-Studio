
from __future__ import annotations
import streamlit as st
from pathlib import Path

from components.resume_builder import render_resume_builder
from components.dashboard import render_dashboard
from components.job_match import render_job_match
from components.resume_improvement import render_resume_improvement
from components.resume_templates import render_resume_templates
from components.resume_export import render_resume_export

from utils.repository import ResumeRepository
from utils.app_state import initialize_app_state
from utils.ats_analyzer import analyze_resume_ats
from utils.resume_text import resume_to_text, resume_to_sections
from utils.config import RESUME_DB_PATH

st.set_page_config(
    page_title="AI Resume Studio",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
        .main-title { font-size: 2.4rem; font-weight: 700; margin-bottom: 0.2rem; }
        .subtitle { color: #6b7280; font-size: 1rem; margin-bottom: 1.5rem; }
        .section-title { font-size: 1.6rem; font-weight: 650; margin-top: 0.5rem; }
        .stButton button { width: 100%; }
    </style>
""", unsafe_allow_html=True)

def render_sidebar() -> str:
    st.sidebar.title("📄 AI Resume Studio")
    st.sidebar.caption("Build, analyze, improve, and export professional resumes.")

    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📝 Resume Builder",
            "📊 Resume Analysis",
            "🎯 Job Match",
            "✨ Resume Improvement",
            "🎨 Templates",
            "📥 Export",
        ],
        key="navigation_radio"
    )

    st.sidebar.divider()

    # Auto-save indicator
    render_auto_save_indicator()

    st.sidebar.divider()

    if st.session_state.get("active_resume_name"):
        st.sidebar.caption(f"Active Resume: {st.session_state.active_resume_name}")

    if st.session_state.get("resume_dirty", False):
        st.sidebar.warning("⚠️ Unsaved changes")

    st.sidebar.caption("AI Resume Studio v1.0")
    st.sidebar.caption("Modular Resume Intelligence Platform")

    return page

def render_home() -> None:
    st.markdown('<div class="main-title">AI Resume Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Build smarter resumes with AI-powered analysis and optimization.</div>', unsafe_allow_html=True)
    render_dashboard()

def render_builder() -> None:
    st.markdown('<div class="section-title">📝 Resume Builder</div>', unsafe_allow_html=True)
    render_resume_builder()

def render_analysis() -> None:
    st.markdown('<div class="section-title">📊 Resume Analysis</div>', unsafe_allow_html=True)
    st.write("Analyze your resume for ATS compatibility, section completeness, keywords, readability, and formatting.")

    resume = st.session_state.resume_data
    job_description = st.text_area("Target Job Description (optional)", placeholder="Paste the target job description here...", height=180, key="ats_job_description")

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🔍 Analyze Resume", type="primary", use_container_width=True):
            resume_text = resume_to_text(resume)
            resume_sections = resume_to_sections(resume)
            result = analyze_resume_ats(resume_text=resume_text, resume_sections=resume_sections, job_description=job_description)
            st.session_state.ats_analysis_result = result
            st.rerun()

    result = st.session_state.get("ats_analysis_result")
    if result:
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("ATS Score", f"{result['score_out_of_100']} / 100")
        with col2:
            st.metric("Keyword Match", f"{result['keyword_match'].get('match_percentage', 0):.1f}%")
        with col3:
            st.metric("Skill Match", f"{result['skills_match'].get('match_percentage', 0):.1f}%")

        st.subheader("Score Breakdown")
        breakdown = result["breakdown"]
        cols = st.columns(3)
        for index, (name, data) in enumerate(breakdown.items()):
            with cols[index % 3]:
                st.metric(name.replace("_", " ").title(), f"{data['score']:.1f} / {data['max_score']}")

        st.subheader("Recommendations")
        for recommendation in result["recommendations"]:
            st.info(f"→ {recommendation}")

        if result["keyword_match"]["job_description_provided"]:
            st.subheader("Keyword Match Details")
            keyword_data = result["keyword_match"]
            st.write(f"**Match Percentage:** {keyword_data['match_percentage']:.1f}%")
            if keyword_data["matching"]:
                st.write("**Matching:** " + ", ".join(keyword_data["matching"]))
            if keyword_data["missing"]:
                st.warning("**Missing:** " + ", ".join(keyword_data["missing"]))

        if result["skills_match"]["job_description_provided"]:
            st.subheader("Skill Match Details")
            skill_data = result["skills_match"]
            st.write(f"**Match Percentage:** {skill_data['match_percentage']:.1f}%")
            if skill_data["matching"]:
                st.success("**Matching skills:** " + ", ".join(skill_data["matching"]))
            if skill_data["missing"]:
                st.warning("**Missing skills:** " + ", ".join(skill_data["missing"]))



# ============================================================
# AUTO-SAVE FUNCTIONALITY
# ============================================================

def auto_save_state() -> None:
    """Auto-save the current state to session and localStorage."""
    if st.session_state.get("resume_dirty", False):
        # Check if we have an active resume ID
        if st.session_state.active_resume_id:
            from utils.app_state import save_active_resume
            save_active_resume()
        else:
            # Create a new draft
            from utils.app_state import save_current_as_draft
            save_current_as_draft()

def get_unsaved_warning() -> str:
    """Get unsaved changes warning message."""
    if st.session_state.get("resume_dirty", False):
        return "⚠️ Unsaved changes"
    return "✅ All changes saved"

# Add auto-save to sidebar
def render_auto_save_indicator() -> None:
    """Render auto-save indicator in sidebar."""
    status = get_unsaved_warning()
    if "Unsaved" in status:
        st.sidebar.warning(status)
    else:
        st.sidebar.success(status)
    
    # Auto-save button
    if st.sidebar.button("💾 Save Now", use_container_width=True):
        from utils.app_state import save_active_resume
        if save_active_resume():
            st.sidebar.success("✅ Saved!")
            st.rerun()


def main() -> None:
    repository = ResumeRepository(RESUME_DB_PATH)
    initialize_app_state(repository)

    page = render_sidebar()

    if page == "🏠 Dashboard":
        render_home()
    elif page == "📝 Resume Builder":
        render_builder()
    elif page == "📊 Resume Analysis":
        render_analysis()
    elif page == "🎯 Job Match":
        render_job_match()
    elif page == "✨ Resume Improvement":
        render_resume_improvement()
    elif page == "🎨 Templates":
        render_resume_templates()
    elif page == "📥 Export":
        render_resume_export()

if __name__ == "__main__":
    main()
