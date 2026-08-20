
from __future__ import annotations
import streamlit as st
from utils.resume_improver import generate_improvement_report
from utils.data_models import WorkExperience, Project

def render_resume_improvement() -> None:
    st.markdown('<div class="section-title">✨ Resume Improvement</div>', unsafe_allow_html=True)
    st.write("Identify weak bullets, generic wording, missing metrics, and opportunities for stronger resume language.")

    resume = st.session_state.resume_data

    if not resume:
        st.info("Please create or load a resume in the Resume Builder first.")
        return

    summary = resume.summary

    experience_bullets = []
    for exp in resume.experience:
        if isinstance(exp, WorkExperience):
            experience_bullets.extend(exp.bullet_points)
        else:
            experience_bullets.extend(exp.get("bullet_points", []))

    project_bullets = []
    for proj in resume.projects:
        if isinstance(proj, Project):
            project_bullets.extend(proj.bullet_points)
        else:
            project_bullets.extend(proj.get("bullet_points", []))

    if st.button("✨ Analyze for Improvements", type="primary", key="run_improvement_analysis"):
        try:
            report = generate_improvement_report(
                summary=summary,
                experience_bullets=experience_bullets,
                project_bullets=project_bullets,
            )
            st.session_state.improvement_report = report
            st.success("Resume improvement analysis completed.")
        except Exception as exc:
            st.error(f"Improvement analysis failed: {exc}")

    report = st.session_state.get("improvement_report")
    if not report:
        return

    st.divider()
    st.subheader("Overall Improvement Score")
    st.metric("Overall Score", f"{report['overall_score']:.1f} / 100")

    st.subheader("Priority Issues")
    if report["priority_issues"]:
        for issue in report["priority_issues"]:
            st.warning(f"⚠️ {issue}")
    else:
        st.info("✓ No major issues detected for improvement.")

    st.subheader("Recommendations")
    if report["recommendations"]:
        for recommendation in report["recommendations"]:
            st.write(f"→ {recommendation}")
    else:
        st.info("✓ No specific recommendations at this time.")

    with st.expander("Detailed Summary Analysis"):
        summary_report = report['summary']
        st.metric("Summary Score", f"{summary_report['score']:.1f} / 100")
        if summary_report['issues']:
            st.write("**Issues:**")
            for issue in summary_report['issues']:
                st.write(f"- {issue}")
        if summary_report['suggestions']:
            st.write("**Suggestions:**")
            for suggestion in summary_report['suggestions']:
                st.write(f"- {suggestion}")

    with st.expander("Detailed Experience Analysis"):
        experience_report = report['experience']
        st.metric("Experience Bullet Score (Avg)", f"{experience_report['overall_score']:.1f} / 100")
        if experience_report['repeated_starters']:
            st.write(f"**Repeated Starters:** {', '.join(experience_report['repeated_starters'])}")
        if experience_report['section_suggestions']:
            st.write("**Section Suggestions:**")
            for suggestion in experience_report['section_suggestions']:
                st.write(f"- {suggestion}")

    with st.expander("Detailed Project Analysis"):
        project_report = report['projects']
        st.metric("Project Bullet Score (Avg)", f"{project_report['overall_score']:.1f} / 100")
        if project_report['repeated_starters']:
            st.write(f"**Repeated Starters:** {', '.join(project_report['repeated_starters'])}")
        if project_report['section_suggestions']:
            st.write("**Section Suggestions:**")
            for suggestion in project_report['section_suggestions']:
                st.write(f"- {suggestion}")
