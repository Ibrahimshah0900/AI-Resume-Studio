
from __future__ import annotations
import copy
import uuid
from typing import Any
import streamlit as st
from utils.repository import ResumeRepository
from utils.resume_manager import ResumeManager
from utils.data_models import Resume

def normalize_resume_data(data: Any) -> Resume:
    if isinstance(data, Resume):
        return data
    if not isinstance(data, dict):
        return Resume()

    normalized = copy.deepcopy(data)
    personal_info = normalized.get("personal_info", {})
    if not isinstance(personal_info, dict):
        personal_info = {}
    if not personal_info.get("email"):
        personal_info["email"] = None
    normalized["personal_info"] = personal_info

    list_fields = ["experience", "education", "skills", "projects", "certifications", "languages", "achievements"]
    for field_name in list_fields:
        value = normalized.get(field_name)
        if not isinstance(value, list):
            normalized[field_name] = []

    try:
        return Resume.model_validate(normalized)
    except Exception:
        return Resume()

def create_empty_resume() -> Resume:
    return Resume()

def initialize_app_state(repository: ResumeRepository) -> None:
    if "repository" not in st.session_state:
        st.session_state.repository = repository
    if "resume_data" not in st.session_state:
        st.session_state.resume_data = create_empty_resume()
    else:
        current = st.session_state.resume_data
        if not isinstance(current, Resume):
            st.session_state.resume_data = normalize_resume_data(current)
    if "active_resume_id" not in st.session_state:
        st.session_state.active_resume_id = None
    if "active_resume_name" not in st.session_state:
        st.session_state.active_resume_name = "Untitled Resume"
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"
    if "resume_dirty" not in st.session_state:
        st.session_state.resume_dirty = False

def create_new_resume(name: str = "Untitled Resume") -> str:
    resume_id = str(uuid.uuid4())
    st.session_state.active_resume_id = resume_id
    st.session_state.active_resume_name = name.strip() or "Untitled Resume"
    st.session_state.resume_data = create_empty_resume()
    st.session_state.resume_dirty = True
    return resume_id

def load_resume(resume_id: str) -> bool:
    repository = st.session_state.repository
    record = repository.get_resume(resume_id)
    if record is None:
        return False
    st.session_state.active_resume_id = record["id"]
    st.session_state.active_resume_name = record["name"]
    st.session_state.resume_data = normalize_resume_data(record["data"])
    st.session_state.resume_dirty = False
    return True

def save_active_resume() -> bool:
    resume_id = st.session_state.active_resume_id
    if not resume_id:
        return False
    repository = st.session_state.repository
    resume = normalize_resume_data(st.session_state.resume_data)
    st.session_state.resume_data = resume
    repository.save_resume(
        resume_id=resume_id,
        name=st.session_state.active_resume_name,
        data=resume.model_dump(mode="json"),
    )
    st.session_state.resume_dirty = False
    return True



from utils.resume_manager import ResumeManager

def initialize_resume_manager() -> ResumeManager:
    """Initialize the resume manager."""
    if "resume_manager" not in st.session_state:
        st.session_state.resume_manager = ResumeManager()
    return st.session_state.resume_manager

def save_current_as_draft(name: str = None) -> bool:
    """Save the current resume as a draft."""
    manager = st.session_state.resume_manager
    resume = normalize_resume_data(st.session_state.resume_data)
    resume_dict = resume.model_dump(mode="json")
    
    if name is None:
        name = st.session_state.active_resume_name
    
    # Check if we're updating an existing draft
    if st.session_state.active_resume_id:
        existing = manager.get_draft(st.session_state.active_resume_id)
        if existing:
            manager.update_draft(st.session_state.active_resume_id, resume_dict, name)
            st.session_state.resume_dirty = False
            return True
    
    # Create new draft
    draft_id = manager.create_draft(name, resume_dict)
    st.session_state.active_resume_id = draft_id
    st.session_state.active_resume_name = name
    st.session_state.resume_dirty = False
    return True

def load_draft_into_state(draft_id: str) -> bool:
    """Load a draft into the current session state."""
    manager = st.session_state.resume_manager
    draft = manager.get_draft(draft_id)
    
    if not draft:
        return False
    
    resume = normalize_resume_data(draft["data"])
    st.session_state.resume_data = resume
    st.session_state.active_resume_id = draft["id"]
    st.session_state.active_resume_name = draft["name"]
    st.session_state.resume_dirty = False
    return True

def delete_draft_from_manager(draft_id: str) -> bool:
    """Delete a draft from the manager."""
    manager = st.session_state.resume_manager
    return manager.delete_draft(draft_id)
def mark_resume_dirty() -> None:
    st.session_state.resume_dirty = True
