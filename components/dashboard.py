
from __future__ import annotations
import streamlit as st
import uuid
from utils.app_state import create_new_resume, load_resume, save_active_resume
from utils.completion_engine import calculate_completion

def _get_completion_percentage(resume_data) -> float:
    try:
        result = calculate_completion(resume_data)
        if isinstance(result, dict):
            return float(result.get("overall_percentage", 0))
        return float(result)
    except Exception:
        return 0.0

def render_dashboard() -> None:
    repository = st.session_state.repository
    resumes = repository.list_resumes()

    st.title("AI Resume Studio")
    st.caption("Build, analyze, optimize, and manage your professional resumes.")

    total_resumes = len(resumes)
    latest_name = resumes[0]["name"] if resumes else "No resumes yet"
    active_completion = _get_completion_percentage(st.session_state.resume_data)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Resumes", total_resumes)
    with col2:
        st.metric("Current Completion", f"{active_completion:.0f}%")
    with col3:
        st.metric("Last Edited", latest_name)

    st.divider()

    if st.session_state.active_resume_id:
        st.subheader("Continue Editing")
        st.write(f"**{st.session_state.active_resume_name}**")
        if st.button("Continue Editing", type="primary", use_container_width=True):
            st.session_state.current_page = "Create Resume"
            st.rerun()

    st.subheader("Create a Resume")

    # Create resume with title prompt
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            new_resume_title = st.text_input(
                "Resume Title",
                placeholder="Enter a title for your new resume...",
                key="new_resume_title_input"
            )
        with col2:
            if st.button(
                "+ Create New Resume",
                use_container_width=True,
                type="primary"
            ):
                title = st.session_state.get("new_resume_title_input", "").strip()
                if not title:
                    st.warning("⚠️ Please enter a title for your resume.")
                else:
                    create_new_resume(title)
                    save_active_resume()
                    st.session_state.current_page = "Create Resume"
                    st.success(f"✅ New resume '{title}' created!")
                    st.rerun()
    st.divider()
    st.subheader("My Resumes")

        if not resumes:
        st.info("📭 You don't have any saved resumes yet.")
        st.markdown("""
        <div style="text-align: center; padding: 40px 20px; background: #f8f9fa; border-radius: 12px; margin: 20px 0;">
            <div style="font-size: 48px; margin-bottom: 16px;">📄</div>
            <h3 style="color: #1a1a1a; margin-bottom: 8px;">No Resumes Yet</h3>
            <p style="color: #6b7280; margin-bottom: 16px;">
                Create your first resume by clicking the button above
            </p>
            <div style="font-size: 14px; color: #9ca3af;">
                💡 You can also load a sample resume from the Resume Builder
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    for resume in resumes:
        resume_id = resume["id"]
        resume_name = resume["name"]

        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([4, 1.5, 1.5, 1.5])

            with col1:
                st.markdown(f"### {resume_name}")
                st.caption(f"Last edited: {resume['updated_at']}")

            with col2:
                if st.button("Open", key=f"open_{resume_id}", use_container_width=True):
                    if load_resume(resume_id):
                        st.session_state.current_page = "Create Resume"
                        st.rerun()
                    else:
                        st.error("Unable to load this resume.")

            with col3:
                if st.button("Duplicate", key=f"duplicate_{resume_id}", use_container_width=True):
                    source = repository.get_resume(resume_id)
                    if source:
                        new_id = str(uuid.uuid4())
                        repository.save_resume(
                            resume_id=new_id,
                            name=f"{source['name']} — Copy",
                            data=source["data"],
                        )
                        st.success("Resume duplicated.")
                        st.rerun()

            with col4:
                if st.button("Delete", key=f"delete_{resume_id}", use_container_width=True):
                    deleted = repository.delete_resume(resume_id)
                    if deleted:
                        if st.session_state.active_resume_id == resume_id:
                            st.session_state.active_resume_id = None
                            st.session_state.active_resume_name = "Untitled Resume"
                        st.success("Resume deleted.")
                        st.rerun()
                    else:
                        st.error("Unable to delete this resume.")