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

    # Custom CSS for beautiful dashboard
    st.markdown('''
    <style>
        .dashboard-title {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1a1a2e;
            margin-bottom: 0.2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .dashboard-subtitle {
            color: #6b7280;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            border: 1px solid #e5e7eb;
            text-align: center;
            transition: transform 0.2s;
        }
        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        .stat-number {
            font-size: 2.2rem;
            font-weight: 700;
            color: #1a1a2e;
        }
        .stat-label {
            color: #6b7280;
            font-size: 0.9rem;
        }
        .resume-card {
            background: white;
            padding: 16px 20px;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            margin-bottom: 10px;
            transition: all 0.2s;
        }
        .resume-card:hover {
            border-color: #667eea;
            box-shadow: 0 2px 12px rgba(102, 126, 234, 0.15);
        }
        .resume-name {
            font-size: 1.1rem;
            font-weight: 600;
            color: #1a1a2e;
        }
        .resume-meta {
            color: #6b7280;
            font-size: 0.85rem;
        }
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 16px;
        }
        .empty-icon {
            font-size: 64px;
            margin-bottom: 16px;
        }
        .empty-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #1a1a2e;
            margin-bottom: 8px;
        }
        .empty-text {
            color: #6b7280;
            font-size: 1rem;
        }
        .continue-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 12px;
            color: white;
            text-align: center;
        }
        .continue-title {
            font-size: 1.2rem;
            font-weight: 600;
        }
        .continue-sub {
            font-size: 0.9rem;
            opacity: 0.9;
        }
    </style>
    ''', unsafe_allow_html=True)

    # Header
    st.markdown('<div class="dashboard-title">📄 Resume Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-subtitle">Create, manage, and export your professional resumes</div>', unsafe_allow_html=True)

    # Statistics Row
    col1, col2, col3 = st.columns(3)
    
    total_resumes = len(resumes)
    active_completion = _get_completion_percentage(st.session_state.resume_data)

    with col1:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-number">{total_resumes}</div>
            <div class="stat-label">📁 Saved Resumes</div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-number">{int(active_completion)}%</div>
            <div class="stat-label">📊 Current Completion</div>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        latest_name = resumes[0]["name"] if resumes else "No resumes"
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-number" style="font-size: 1.2rem;">{latest_name[:20]}</div>
            <div class="stat-label">📝 Last Edited</div>
        </div>
        ''', unsafe_allow_html=True)

    st.divider()

    # Create New Resume Section
    st.markdown("### ✨ Create New Resume")
    col1, col2 = st.columns([3, 1])
    with col1:
        new_title = st.text_input(
            "Resume Title",
            placeholder="Enter a title for your new resume...",
            key="new_resume_title_input",
            label_visibility="collapsed"
        )
    with col2:
        if st.button("➕ Create", type="primary", use_container_width=True):
            title = st.session_state.get("new_resume_title_input", "").strip()
            if not title:
                st.warning("⚠️ Please enter a title")
            else:
                create_new_resume(title)
                save_active_resume()
                st.session_state.current_page = "Create Resume"
                st.success(f"✅ '{title}' created!")
                st.rerun()

    st.divider()

    # My Resumes Section
    st.markdown("### 📂 My Resumes")

    if not resumes:
        st.markdown('''
        <div class="empty-state">
            <div class="empty-icon">📄</div>
            <div class="empty-title">No Resumes Yet</div>
            <div class="empty-text">Create your first resume by entering a title above and clicking "Create"</div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        for resume in resumes:
            resume_id = resume["id"]
            resume_name = resume["name"]

            # Get completion for this resume
            try:
                resume_data = repository.get_resume(resume_id)
                if resume_data:
                    comp = calculate_completion(resume_data["data"])
                    comp_percent = comp.get("overall_percentage", 0) if isinstance(comp, dict) else 0
                else:
                    comp_percent = 0
            except:
                comp_percent = 0

            # Resume card with buttons
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write(f"**{resume_name}**")
                st.caption(f"📅 {resume['updated_at'][:16]} · 📊 {comp_percent}% complete")
            with col2:
                if st.button("✏️ Edit", key=f"edit_{resume_id}", use_container_width=True):
                    if load_resume(resume_id):
                        st.session_state.current_page = "Create Resume"
                        st.rerun()
                    else:
                        st.error("Unable to load")
            with col3:
                if st.button("📥 Download", key=f"dl_{resume_id}", use_container_width=True):
                    if load_resume(resume_id):
                        st.session_state.current_page = "Export"
                        st.rerun()
                    else:
                        st.error("Unable to load")
            with col4:
                if st.button("🗑️ Delete", key=f"del_{resume_id}", use_container_width=True):
                    deleted = repository.delete_resume(resume_id)
                    if deleted:
                        if st.session_state.active_resume_id == resume_id:
                            st.session_state.active_resume_id = None
                            st.session_state.active_resume_name = "Untitled Resume"
                        st.success("✅ Resume deleted!")
                        st.rerun()
                    else:
                        st.error("Unable to delete")

    st.divider()
    
    # Continue Editing Section (if active resume exists)
    if st.session_state.active_resume_id:
        st.markdown(f'''
        <div class="continue-card">
            <div class="continue-title">✏️ Continue Editing</div>
            <div class="continue-sub">{st.session_state.active_resume_name}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("📝 Continue Editing", type="primary", use_container_width=True):
            st.session_state.current_page = "Create Resume"
            st.rerun()
