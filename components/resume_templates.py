
from __future__ import annotations
import streamlit as st
from utils.template_engine import get_template_summary, DEFAULT_TEMPLATE_ID

def render_resume_templates() -> None:
    st.markdown('<div class="section-title">🎨 Resume Templates</div>', unsafe_allow_html=True)
    st.write("Browse and select from our professional resume templates. Each template is designed to optimize readability and impact.")

    templates = get_template_summary()
    current_selected_template_id = st.session_state.get("selected_template_id", DEFAULT_TEMPLATE_ID)

    # Display templates as cards with visual preview
    cols = st.columns(3)
    
    for idx, template in enumerate(templates):
        with cols[idx % 3]:
            with st.container(border=True):
                is_selected = template["id"] == current_selected_template_id
                
                # Template preview box (visual representation)
                st.markdown(f"""
                <div style="border: {'3px solid #2563eb' if is_selected else '1px solid #ddd'}; 
                            border-radius: 8px; 
                            padding: 12px; 
                            background: {'#f0f7ff' if is_selected else 'white'};
                            min-height: 200px;">
                    <div style="border-bottom: 2px solid {'#2563eb' if is_selected else '#ccc'}; 
                                padding-bottom: 8px; 
                                margin-bottom: 8px;">
                        <strong style="font-size: 16px;">{template['name']}</strong>
                    </div>
                    <div style="font-size: 10px; color: #666; line-height: 1.6;">
                        <div style="background: {'#e8f0fe' if is_selected else '#f5f5f5'}; 
                                    padding: 4px 8px; 
                                    border-radius: 4px; 
                                    margin-bottom: 4px;">
                            <b>Sample Resume</b>
                        </div>
                        <div style="padding-left: 8px; border-left: 3px solid {'#2563eb' if is_selected else '#ddd'};">
                            <div>• Professional Experience</div>
                            <div>• Skills Section</div>
                            <div>• Education</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.caption(template['description'][:80] + "...")
                st.caption(f"**Category:** {template['category']}")
                st.caption(f"**ATS Friendly:** {'✅' if template['ats_friendly'] else '❌'}")
                
                if st.button(
                    f"{'✅ Selected' if is_selected else 'Select'}", 
                    key=f"select_{template['id']}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    st.session_state.selected_template_id = template["id"]
                    st.rerun()

    st.divider()
    st.subheader("Template Details")

    selected_template_details = next((t for t in templates if t["id"] == current_selected_template_id), None)

    if selected_template_details:
        st.write(f"**Name:** {selected_template_details['name']}")
        st.write(f"**Description:** {selected_template_details['description']}")
        st.write(f"**Category:** {selected_template_details['category']}")
        st.write(f"**ATS Friendly:** {'Yes' if selected_template_details['ats_friendly'] else 'No'}")
        st.write(f"**Recommended For:** {', '.join(selected_template_details['recommended_for'])}")

    st.info("The selected template will be applied when you export your resume.")
